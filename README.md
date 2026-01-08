# PDF Toolkit SaaS

A complete, production-ready PDF toolkit SaaS application with user authentication, subscription payments, and usage tracking.

## Features

- **PDF Tools:**
  - Merge multiple PDFs
  - Split PDFs into pages
  - Compress PDFs
  - Convert images to PDF

- **User Management:**
  - User registration & authentication
  - Subscription tiers (Free, Basic, Pro)
  - Usage tracking & limits

- **Payment Integration:**
  - Stripe subscription payments
  - Automatic tier management
  - Webhook handling

- **Admin Dashboard:**
  - User statistics
  - Operation tracking
  - Revenue metrics

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A Stripe account (for payments)

### Installation & Setup

1. **Navigate to the project directory:**
   ```bash
   cd pdf-toolkit-saas
   ```

2. **Run the setup script:**

   **On Windows:**
   ```bash
   setup.bat
   ```

   **On Mac/Linux:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   This will:
   - Create a virtual environment
   - Install all dependencies
   - Set up the database
   - Create a `.env` file from the template

3. **Configure your Stripe keys:**

   - Go to https://dashboard.stripe.com/apikeys
   - Copy your API keys
   - Open `.env` file and update:
     ```
     STRIPE_PUBLIC_KEY=your_public_key_here
     STRIPE_SECRET_KEY=your_secret_key_here
     ```

4. **Create Stripe products (one-time setup):**

   - Go to https://dashboard.stripe.com/products
   - Create two products:
     1. "Basic Plan" - $9/month recurring
     2. "Pro Plan" - $29/month recurring
   - Copy the Price IDs and update in `.env`:
     ```
     STRIPE_PRICE_BASIC=price_xxxxx
     STRIPE_PRICE_PRO=price_xxxxx
     ```

5. **Run the application:**

   **On Windows:**
   ```bash
   start.bat
   ```

   **On Mac/Linux:**
   ```bash
   ./start.sh
   ```

6. **Access the application:**

   Open your browser and go to: http://localhost:5000

## Usage

### For Development

1. Create an account at http://localhost:5000/register
2. Login and start using the PDF tools
3. Free tier gives you 5 operations per month

### For Production Deployment

See `DEPLOYMENT.md` for detailed deployment instructions.

## Project Structure

```
pdf-toolkit-saas/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── config.py              # Configuration
├── pdf_utils.py           # PDF processing utilities
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from .env.example)
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── merge.html
│   ├── split.html
│   ├── compress.html
│   ├── convert.html
│   ├── pricing.html
│   └── admin.html
├── static/                # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── uploads/               # Temporary file storage

```

## Subscription Tiers

| Feature | Free | Basic ($9/mo) | Pro ($29/mo) |
|---------|------|---------------|--------------|
| Operations/month | 5 | 100 | 1000 |
| Max file size | 10MB | 50MB | 100MB |
| All PDF tools | ✓ | ✓ | ✓ |
| Priority support | - | ✓ | ✓ |
| API access | - | - | ✓ |

## Admin Access

To access the admin dashboard:

1. Create an account with email: `admin@pdftoolkit.com`
2. Go to: http://localhost:5000/admin

Or update the admin email check in `app.py` line 285:
```python
if current_user.email != 'your-admin-email@example.com':
```

## Environment Variables

- `FLASK_SECRET_KEY` - Secret key for sessions (change in production!)
- `DATABASE_URL` - Database connection string
- `STRIPE_PUBLIC_KEY` - Stripe publishable key
- `STRIPE_SECRET_KEY` - Stripe secret key
- `STRIPE_WEBHOOK_SECRET` - Stripe webhook signing secret
- `STRIPE_PRICE_BASIC` - Stripe price ID for Basic tier
- `STRIPE_PRICE_PRO` - Stripe price ID for Pro tier

## Stripe Webhook Setup (For Production)

1. Go to https://dashboard.stripe.com/webhooks
2. Add endpoint: `https://yourdomain.com/webhook`
3. Select events:
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
4. Copy the webhook signing secret to `.env`

## Troubleshooting

### "Module not found" errors
- Make sure you activated the virtual environment
- Run: `pip install -r requirements.txt`

### Database errors
- Delete `pdftoolkit.db` and restart the application
- It will recreate the database automatically

### Stripe errors
- Double-check your API keys in `.env`
- Make sure you're using the correct keys (test vs live)
- Verify the Price IDs match your Stripe products

## Security Notes

⚠️ **Before deploying to production:**

1. Change `FLASK_SECRET_KEY` to a strong random value
2. Use a production database (PostgreSQL recommended)
3. Enable HTTPS
4. Set up proper CORS policies
5. Configure file size limits
6. Set up file cleanup cron jobs
7. Add rate limiting
8. Review and update security headers

## Making Money

### Revenue Potential

With this setup, here's how you can reach $1000/month:

- **Basic Plan ($9/mo):** Need ~55 customers
- **Pro Plan ($29/mo):** Need ~35 customers
- **Mix (50/50):** Need ~53 customers total

### Marketing Ideas

1. **SEO & Content:**
   - Write blog posts about PDF tips
   - Target keywords like "merge pdf online", "compress pdf"
   - Create tutorial videos

2. **Product Hunt Launch:**
   - Launch on Product Hunt
   - Get initial users and feedback

3. **Reddit/Forums:**
   - Help people in r/productivity, r/smallbusiness
   - Share your tool when relevant

4. **Social Media:**
   - Share PDF tips on Twitter
   - Create LinkedIn content for professionals

5. **Partnerships:**
   - Partner with productivity tools
   - Offer white-label version

## Support

For issues or questions:
- Check the troubleshooting section
- Review the code comments
- Check Stripe dashboard for payment issues

## License

Proprietary - All rights reserved.

---

Built with Flask, Python, and Stripe. Ready to deploy and start earning revenue!
