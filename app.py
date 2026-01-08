import os
import io
import stripe
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
from models import db, User, PDFOperation
from pdf_utils import PDFProcessor
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize Stripe
stripe.api_key = app.config['STRIPE_SECRET_KEY']

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def allowed_file(filename, allowed_types=None):
    if allowed_types is None:
        allowed_types = app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_types


# ==================== ROUTES ====================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))

        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash('Registration successful!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    operations = PDFOperation.query.filter_by(user_id=current_user.id).order_by(PDFOperation.created_at.desc()).limit(10).all()
    return render_template('dashboard.html', user=current_user, operations=operations)


# ==================== PDF OPERATIONS ====================

@app.route('/merge', methods=['GET', 'POST'])
@login_required
def merge_pdfs():
    if request.method == 'GET':
        return render_template('merge.html', user=current_user)

    # Check usage limit
    if not current_user.can_perform_operation():
        return jsonify({'error': 'Usage limit reached. Please upgrade your plan.'}), 403

    files = request.files.getlist('files')
    if len(files) < 2:
        return jsonify({'error': 'Please upload at least 2 PDF files'}), 400

    try:
        # Validate files
        for file in files:
            if not file or not allowed_file(file.filename, {'pdf'}):
                return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400

        # Process merge
        merged_pdf = PDFProcessor.merge_pdfs(files)

        # Log operation
        operation = PDFOperation(
            user_id=current_user.id,
            operation_type='merge',
            file_count=len(files)
        )
        db.session.add(operation)
        current_user.increment_usage()

        # Return file
        return send_file(
            merged_pdf,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'merged_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/split', methods=['GET', 'POST'])
@login_required
def split_pdf():
    if request.method == 'GET':
        return render_template('split.html', user=current_user)

    if not current_user.can_perform_operation():
        return jsonify({'error': 'Usage limit reached. Please upgrade your plan.'}), 403

    file = request.files.get('file')
    if not file or not allowed_file(file.filename, {'pdf'}):
        return jsonify({'error': 'Please upload a valid PDF file'}), 400

    try:
        # Get split options
        split_type = request.form.get('split_type', 'all')

        if split_type == 'all':
            # Split each page
            outputs = PDFProcessor.split_pdf(file)
        else:
            # Custom page ranges (not implemented in this version for simplicity)
            outputs = PDFProcessor.split_pdf(file)

        # For simplicity, return first split page (you can extend to zip multiple)
        operation = PDFOperation(
            user_id=current_user.id,
            operation_type='split',
            file_count=len(outputs)
        )
        db.session.add(operation)
        current_user.increment_usage()

        return send_file(
            outputs[0],
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'split_page_1_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/compress', methods=['GET', 'POST'])
@login_required
def compress_pdf():
    if request.method == 'GET':
        return render_template('compress.html', user=current_user)

    if not current_user.can_perform_operation():
        return jsonify({'error': 'Usage limit reached. Please upgrade your plan.'}), 403

    file = request.files.get('file')
    if not file or not allowed_file(file.filename, {'pdf'}):
        return jsonify({'error': 'Please upload a valid PDF file'}), 400

    try:
        quality = request.form.get('quality', 'medium')
        compressed_pdf = PDFProcessor.compress_pdf(file, quality)

        operation = PDFOperation(
            user_id=current_user.id,
            operation_type='compress',
            file_count=1
        )
        db.session.add(operation)
        current_user.increment_usage()

        return send_file(
            compressed_pdf,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'compressed_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/convert', methods=['GET', 'POST'])
@login_required
def convert_to_pdf():
    if request.method == 'GET':
        return render_template('convert.html', user=current_user)

    if not current_user.can_perform_operation():
        return jsonify({'error': 'Usage limit reached. Please upgrade your plan.'}), 403

    files = request.files.getlist('files')
    if not files:
        return jsonify({'error': 'Please upload at least one image file'}), 400

    try:
        # Validate files
        for file in files:
            if not file or not allowed_file(file.filename, {'png', 'jpg', 'jpeg'}):
                return jsonify({'error': 'Invalid file type. Only PNG, JPG, JPEG are allowed.'}), 400

        # Convert images to PDF
        pdf_output = PDFProcessor.image_to_pdf(files)

        operation = PDFOperation(
            user_id=current_user.id,
            operation_type='convert',
            file_count=len(files)
        )
        db.session.add(operation)
        current_user.increment_usage()

        return send_file(
            pdf_output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'converted_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== PRICING & SUBSCRIPTION ====================

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')


@app.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    data = request.get_json()
    price_id = data.get('price_id')

    try:
        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            customer_email=current_user.email,
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=url_for('subscription_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('pricing', _external=True),
            metadata={
                'user_id': current_user.id
            }
        )

        return jsonify({'checkout_url': checkout_session.url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/subscription-success')
@login_required
def subscription_success():
    session_id = request.args.get('session_id')

    if session_id:
        try:
            # Retrieve the session
            session = stripe.checkout.Session.retrieve(session_id)

            # Update user subscription
            current_user.stripe_customer_id = session.customer
            current_user.stripe_subscription_id = session.subscription

            # Determine tier based on price
            subscription = stripe.Subscription.retrieve(session.subscription)
            price_id = subscription['items']['data'][0]['price']['id']

            if price_id == app.config['STRIPE_PRICE_BASIC']:
                current_user.subscription_tier = 'basic'
            elif price_id == app.config['STRIPE_PRICE_PRO']:
                current_user.subscription_tier = 'pro'

            current_user.subscription_status = 'active'
            db.session.commit()

            flash('Subscription successful! Welcome to your new plan.', 'success')

        except Exception as e:
            flash(f'Error processing subscription: {str(e)}', 'error')

    return redirect(url_for('dashboard'))


@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhooks"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, app.config['STRIPE_WEBHOOK_SECRET']
        )

        # Handle subscription updates
        if event['type'] == 'customer.subscription.updated':
            subscription = event['data']['object']
            user = User.query.filter_by(stripe_subscription_id=subscription['id']).first()

            if user:
                user.subscription_status = subscription['status']
                db.session.commit()

        elif event['type'] == 'customer.subscription.deleted':
            subscription = event['data']['object']
            user = User.query.filter_by(stripe_subscription_id=subscription['id']).first()

            if user:
                user.subscription_tier = 'free'
                user.subscription_status = 'canceled'
                db.session.commit()

        return jsonify({'status': 'success'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# ==================== ADMIN ====================

@app.route('/admin')
@login_required
def admin():
    # Simple admin check (you can add a proper role system)
    if current_user.email != 'admin@pdftoolkit.com':  # Change this to your admin email
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))

    total_users = User.query.count()
    total_operations = PDFOperation.query.count()
    paid_users = User.query.filter(User.subscription_tier != 'free').count()

    recent_operations = PDFOperation.query.order_by(PDFOperation.created_at.desc()).limit(20).all()

    stats = {
        'total_users': total_users,
        'paid_users': paid_users,
        'total_operations': total_operations,
        'operations': recent_operations
    }

    return render_template('admin.html', stats=stats)


# ==================== API ENDPOINTS ====================

@app.route('/api/usage')
@login_required
def api_usage():
    """Get current usage stats for the user"""
    return jsonify({
        'usage_count': current_user.usage_count,
        'usage_limit': current_user.get_usage_limit(),
        'subscription_tier': current_user.subscription_tier,
        'can_perform': current_user.can_perform_operation()
    })


# ==================== ERROR HANDLERS ====================

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File too large. Maximum size is 10MB.'}), 413


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


# ==================== INITIALIZATION ====================

def init_db():
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")


# Initialize database tables on startup (works in both dev and production)
with app.app_context():
    db.create_all()
    print("Database tables created/verified!")


if __name__ == '__main__':
    # Run the app (only for local development)
    print("=" * 50)
    print("PDF Toolkit SaaS is starting...")
    print("=" * 50)
    print(f"Access the app at: http://localhost:5000")
    print("=" * 50)

    app.run(debug=True, host='0.0.0.0', port=5000)
