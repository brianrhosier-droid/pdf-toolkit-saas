# Deployment Guide

This guide will help you deploy your PDF Toolkit SaaS to production.

## Deployment Options

### Option 1: DigitalOcean App Platform (Recommended - Easiest)

**Cost:** ~$12-25/month
**Difficulty:** Easy
**Setup Time:** 15 minutes

1. **Prepare your code:**
   ```bash
   # Create a git repository
   git init
   git add .
   git commit -m "Initial commit"

   # Push to GitHub (create a repo first)
   git remote add origin https://github.com/yourusername/pdf-toolkit.git
   git push -u origin main
   ```

2. **Deploy to DigitalOcean:**
   - Go to https://cloud.digitalocean.com/apps
   - Click "Create App"
   - Connect your GitHub repository
   - DigitalOcean will auto-detect it's a Python app
   - Configure environment variables (from your .env file)
   - Click "Deploy"

3. **Set up database:**
   - In App Platform, add a PostgreSQL database
   - Update DATABASE_URL environment variable

4. **Configure domain:**
   - Add your custom domain in App Platform settings
   - Update DNS records as instructed

### Option 2: Heroku

**Cost:** ~$16/month (Eco dyno + Postgres)
**Difficulty:** Easy
**Setup Time:** 20 minutes

1. **Install Heroku CLI:**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku app:**
   ```bash
   heroku login
   heroku create your-pdf-toolkit
   ```

3. **Add PostgreSQL:**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Set environment variables:**
   ```bash
   heroku config:set FLASK_SECRET_KEY=your-secret-key
   heroku config:set STRIPE_PUBLIC_KEY=your-stripe-key
   heroku config:set STRIPE_SECRET_KEY=your-stripe-secret
   # ... add all other variables
   ```

5. **Create Procfile:**
   ```
   web: gunicorn app:app
   ```

6. **Deploy:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

7. **Initialize database:**
   ```bash
   heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

### Option 3: Railway

**Cost:** Free tier available, ~$5-20/month paid
**Difficulty:** Easy
**Setup Time:** 10 minutes

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Connect your GitHub repository
4. Add PostgreSQL database
5. Set environment variables
6. Railway will auto-deploy

### Option 4: AWS EC2 (Most Control)

**Cost:** ~$10-30/month
**Difficulty:** Advanced
**Setup Time:** 1-2 hours

See detailed AWS guide below.

## Production Checklist

Before deploying, make sure you:

- [ ] Change `FLASK_SECRET_KEY` to a strong random value
- [ ] Update database to PostgreSQL (not SQLite)
- [ ] Set `FLASK_ENV=production`
- [ ] Configure proper CORS settings
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure Stripe webhook URL
- [ ] Set up domain name
- [ ] Add file cleanup cronjob
- [ ] Configure error monitoring (e.g., Sentry)
- [ ] Set up backups for database
- [ ] Update admin email in app.py
- [ ] Add privacy policy and terms of service
- [ ] Test all payment flows with Stripe test mode
- [ ] Switch to Stripe live mode when ready

## Database Migration (SQLite to PostgreSQL)

1. **Install PostgreSQL locally or use cloud provider**

2. **Update requirements.txt:**
   ```
   psycopg2-binary==2.9.9
   ```

3. **Update DATABASE_URL in .env:**
   ```
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   ```

4. **Run migration:**
   ```python
   from app import app, db
   with app.app_context():
       db.create_all()
   ```

## Stripe Webhook Configuration

1. **Get your webhook URL:**
   - Production URL: `https://yourdomain.com/webhook`

2. **Add webhook in Stripe:**
   - Go to https://dashboard.stripe.com/webhooks
   - Click "Add endpoint"
   - Enter your webhook URL
   - Select events:
     - `customer.subscription.updated`
     - `customer.subscription.deleted`
     - `checkout.session.completed`

3. **Update webhook secret:**
   - Copy the webhook signing secret
   - Add to environment variables: `STRIPE_WEBHOOK_SECRET`

## File Storage

For production, consider using cloud storage:

### AWS S3

1. **Install boto3:**
   ```bash
   pip install boto3
   ```

2. **Update pdf_utils.py to save to S3 instead of local disk**

3. **Set environment variables:**
   ```
   AWS_ACCESS_KEY_ID=your-key
   AWS_SECRET_ACCESS_KEY=your-secret
   AWS_S3_BUCKET=your-bucket
   ```

### Or use DigitalOcean Spaces, Cloudinary, etc.

## File Cleanup

Add a cron job to clean up temporary files:

```python
# cleanup.py
import os
import time
from datetime import datetime, timedelta

UPLOAD_FOLDER = 'uploads'
MAX_AGE_HOURS = 1

for filename in os.listdir(UPLOAD_FOLDER):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.isfile(filepath):
        file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
        if datetime.now() - file_modified > timedelta(hours=MAX_AGE_HOURS):
            os.remove(filepath)
            print(f"Deleted old file: {filename}")
```

**Set up cron job:**
```bash
# Run every hour
0 * * * * cd /path/to/app && python cleanup.py
```

## Monitoring & Analytics

### Error Monitoring (Sentry)

1. **Install Sentry:**
   ```bash
   pip install sentry-sdk[flask]
   ```

2. **Add to app.py:**
   ```python
   import sentry_sdk
   from sentry_sdk.integrations.flask import FlaskIntegration

   sentry_sdk.init(
       dsn="your-sentry-dsn",
       integrations=[FlaskIntegration()]
   )
   ```

### Analytics (Google Analytics)

Add to base.html before `</head>`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## SSL/HTTPS

Most hosting providers (Heroku, DigitalOcean, Railway) provide free SSL certificates automatically.

For custom setup:
- Use Let's Encrypt (free)
- Configure Nginx as reverse proxy
- Force HTTPS redirects

## Performance Optimization

1. **Enable gzip compression**
2. **Use CDN for static files**
3. **Implement caching**
4. **Optimize database queries**
5. **Add rate limiting**

## Scaling Considerations

When you grow beyond 1000 users:

1. **Database:**
   - Upgrade to larger PostgreSQL instance
   - Add read replicas
   - Implement database connection pooling

2. **File Processing:**
   - Move to background jobs (Celery + Redis)
   - Use separate worker dynos/containers

3. **Caching:**
   - Implement Redis for session storage
   - Cache user data and usage counts

4. **Load Balancing:**
   - Use multiple application instances
   - Add load balancer

## Cost Breakdown (Monthly)

**Minimum viable deployment:**
- Hosting: $12 (DigitalOcean App Platform Basic)
- Database: $7 (Managed PostgreSQL)
- Domain: $1/month (amortized)
- **Total: ~$20/month**

**With 100 paying customers ($900/month revenue):**
- Same infrastructure works fine
- **Profit: ~$880/month**

**With 500 paying customers ($4500/month revenue):**
- Hosting: $25 (upgrade instance)
- Database: $15 (larger database)
- CDN/Storage: $10
- Monitoring: $10
- **Total: ~$60/month**
- **Profit: ~$4440/month**

## Support & Maintenance

Budget ~2-5 hours/week for:
- Customer support emails
- Bug fixes
- Feature requests
- Server monitoring

## Going Live Checklist

- [ ] Test all features on production
- [ ] Test payment flow with Stripe test cards
- [ ] Verify webhook is receiving events
- [ ] Test user registration and login
- [ ] Verify email is working
- [ ] Test all PDF operations
- [ ] Check mobile responsiveness
- [ ] Verify analytics are tracking
- [ ] Test error pages (404, 500)
- [ ] Set up monitoring alerts
- [ ] Prepare launch announcement
- [ ] Have privacy policy and terms ready
- [ ] Set up customer support email

## Marketing Your SaaS

Once deployed:

1. **Launch on Product Hunt**
2. **Post on Reddit** (r/SideProject, r/entrepreneur)
3. **Share on Twitter**
4. **Write blog posts** about PDF tips
5. **Create YouTube tutorials**
6. **Run Google Ads** for "pdf merger" etc.
7. **SEO optimization**
8. **Email marketing**

---

Good luck with your SaaS! Remember: ship first, perfect later. Get it live and start getting users!
