from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Subscription info
    subscription_tier = db.Column(db.String(20), default='free')  # free, basic, pro
    stripe_customer_id = db.Column(db.String(100), unique=True)
    stripe_subscription_id = db.Column(db.String(100), unique=True)
    subscription_status = db.Column(db.String(20), default='active')  # active, canceled, past_due

    # Usage tracking
    usage_count = db.Column(db.Integer, default=0)
    usage_reset_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    operations = db.relationship('PDFOperation', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_usage_limit(self):
        limits = {
            'free': 5,
            'basic': 100,
            'pro': 1000
        }
        return limits.get(self.subscription_tier, 5)

    def can_perform_operation(self):
        # Check if usage reset is needed (monthly)
        if self.usage_reset_date:
            days_since_reset = (datetime.utcnow() - self.usage_reset_date).days
            if days_since_reset >= 30:
                self.usage_count = 0
                self.usage_reset_date = datetime.utcnow()
                db.session.commit()

        return self.usage_count < self.get_usage_limit()

    def increment_usage(self):
        self.usage_count += 1
        db.session.commit()

    def __repr__(self):
        return f'<User {self.email}>'


class PDFOperation(db.Model):
    __tablename__ = 'pdf_operations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    operation_type = db.Column(db.String(50), nullable=False)  # merge, split, compress, convert
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_count = db.Column(db.Integer, default=1)
    success = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<PDFOperation {self.operation_type} by User {self.user_id}>'
