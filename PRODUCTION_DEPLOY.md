# Production Deployment Guide - Quick Start

This guide will walk you through deploying your PDF Toolkit SaaS to production in about 30 minutes.

## Prerequisites

- ✅ App running locally (you've done this!)
- GitHub account (free)
- DigitalOcean account (free to create, ~$12/month to run)
- Credit card for DigitalOcean (required but won't be charged until you deploy)

## Step-by-Step Deployment

### Step 1: Create GitHub Account & Repository (5 minutes)

1. **Create GitHub account** (if you don't have one):
   - Go to https://github.com/signup
   - Enter email, password, username
   - Verify email

2. **Create a new repository:**
   - Go to https://github.com/new
   - Repository name: `pdf-toolkit-saas`
   - Description: "PDF processing SaaS application"
   - Select: **Private** (keep your code private)
   - Do NOT initialize with README (we have files already)
   - Click "Create repository"

3. **You'll see instructions** - we'll use them in Step 2!

### Step 2: Push Your Code to GitHub (5 minutes)

Open Git Bash (or your terminal) and run these commands:

```bash
cd pdf-toolkit-saas

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit - PDF Toolkit SaaS"

# Add GitHub as remote (replace YOUR_USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/pdf-toolkit-saas.git

# Push to GitHub
git branch -M main
git push -u origin main
```

If prompted for credentials, use your GitHub username and **personal access token** (not password).

**To create a personal access token:**
- Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
- Generate new token
- Select scopes: `repo` (all)
- Copy the token and use it as password

### Step 3: Create DigitalOcean Account (5 minutes)

1. Go to https://www.digitalocean.com/
2. Click "Sign Up"
3. Create account (can use GitHub to sign up)
4. Add payment method (credit card)
   - New accounts often get $200 free credit for 60 days!

### Step 4: Deploy to DigitalOcean App Platform (10 minutes)

1. **Go to App Platform:**
   - In DigitalOcean dashboard, click "Create" → "Apps"
   - Or go to: https://cloud.digitalocean.com/apps

2. **Connect GitHub:**
   - Choose "GitHub" as source
   - Click "Manage Access" → Authorize DigitalOcean
   - Select your `pdf-toolkit-saas` repository
   - Click "Next"

3. **Configure App:**
   - App name: `pdf-toolkit-saas` (or choose your own)
   - Branch: `main`
   - Autodeploy: ✅ (enable this - auto-deploys on git push)
   - DigitalOcean will auto-detect it's a Python app from Procfile
   - Click "Next"

4. **Add Database:**
   - Click "Add Resource" → "Database"
   - Choose "Dev Database" ($7/month) or "Basic" ($15/month)
   - Name: `pdf-toolkit-db`
   - Click "Add"
   - This automatically creates DATABASE_URL environment variable!

5. **Configure Environment Variables:**
   - Scroll to "Environment Variables"
   - Click "Edit"
   - Add these variables (one by one):

   ```
   FLASK_SECRET_KEY=change-this-to-random-string-in-production
   FLASK_ENV=production
   STRIPE_PUBLIC_KEY=your_stripe_key_here
   STRIPE_SECRET_KEY=your_stripe_secret_here
   STRIPE_WEBHOOK_SECRET=your_webhook_secret_here
   STRIPE_PRICE_BASIC=your_basic_price_id
   STRIPE_PRICE_PRO=your_pro_price_id
   FREE_TIER_LIMIT=5
   BASIC_TIER_LIMIT=100
   PRO_TIER_LIMIT=1000
   MAX_FILE_SIZE_MB=10
   ```

   **Important:** For now, you can use dummy values for Stripe keys. We'll update them later.

6. **Review & Deploy:**
   - Review plan: Should show ~$12-22/month (Basic app + Dev database)
   - Click "Create Resources"
   - Wait 5-10 minutes for deployment...

7. **App is Live! 🎉**
   - You'll get a URL like: `https://pdf-toolkit-saas-xxxxx.ondigitalocean.app`
   - Click the URL to view your live app!

### Step 5: Update FLASK_SECRET_KEY (Important!)

1. **Generate a secure secret key:**
   - Open Python terminal locally:
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```
   - Copy the output

2. **Update in DigitalOcean:**
   - Go to your app → Settings → App-Level Environment Variables
   - Find `FLASK_SECRET_KEY`
   - Replace with the generated key
   - Click "Save"
   - App will redeploy automatically

### Step 6: Set Up Stripe (Optional - For Payments)

If you want to accept payments now:

1. **Create Stripe account:**
   - Go to https://stripe.com
   - Sign up (free)

2. **Get API keys:**
   - Dashboard → Developers → API keys
   - Copy "Publishable key" and "Secret key"

3. **Create products:**
   - Dashboard → Products → Add Product
   - Create "Basic Plan": $9/month, recurring
   - Create "Pro Plan": $29/month, recurring
   - Copy each "Price ID"

4. **Update environment variables in DigitalOcean:**
   - Go to App → Settings → Environment Variables
   - Update all STRIPE_* variables with real values
   - Click "Save" (will redeploy)

5. **Set up webhook:**
   - Stripe Dashboard → Developers → Webhooks
   - Add endpoint: `https://your-app-url.ondigitalocean.app/webhook`
   - Select events:
     - `customer.subscription.updated`
     - `customer.subscription.deleted`
     - `checkout.session.completed`
   - Copy webhook signing secret
   - Update `STRIPE_WEBHOOK_SECRET` in DigitalOcean

## Your App is Live! 🎉

**Your production app is now running at:**
`https://pdf-toolkit-saas-xxxxx.ondigitalocean.app`

### Test Your Production App:

1. ✅ Visit your app URL
2. ✅ Create an account
3. ✅ Test all PDF tools
4. ✅ Try upgrading to Basic plan (if Stripe is configured)
5. ✅ Check admin dashboard

### Next Steps:

1. **Get a custom domain** (optional):
   - Buy domain from Namecheap, Google Domains, etc. (~$10-15/year)
   - In DigitalOcean: App → Settings → Domains
   - Add your domain and follow DNS instructions

2. **Marketing:**
   - Launch on Product Hunt
   - Share on social media
   - Write blog posts
   - Run Google Ads

3. **Monitor:**
   - DigitalOcean shows metrics, logs, errors
   - Set up alerts for downtime

## Costs Breakdown

**Monthly Costs:**
- App (Basic): $12/month
- Database (Dev): $7/month
- **Total: $19/month**

**With first customer at $9/month:**
- Revenue: $9
- Costs: $19
- Net: -$10 (still building)

**At 10 customers (avg $12/month):**
- Revenue: $120
- Costs: $19
- Net profit: **$101/month** ✅

**At 85 customers (goal):**
- Revenue: $1020
- Costs: $19
- Net profit: **$1001/month** 🎉

## Troubleshooting

### Build Failed
- Check logs in DigitalOcean dashboard
- Usually it's a missing dependency or Python version issue
- Fix, commit, push to GitHub - auto-redeploys

### Database Connection Error
- Make sure DATABASE_URL is set (should be automatic)
- Check database is running in DigitalOcean

### App crashes on startup
- Check Runtime Logs in DigitalOcean
- Look for Python errors
- Usually environment variable issues

### Stripe not working
- Verify all STRIPE_* environment variables are set
- Make sure you're using the right keys (test vs live)
- Check webhook is configured correctly

## Updating Your App

Whenever you make changes:

```bash
git add .
git commit -m "Description of changes"
git push
```

DigitalOcean will automatically detect the push and redeploy! 🚀

## Support

- DigitalOcean Docs: https://docs.digitalocean.com/products/app-platform/
- Community: https://www.digitalocean.com/community
- Your app logs: DigitalOcean Dashboard → Your App → Runtime Logs

---

**You're ready to make money! Start marketing and get your first customers!** 💰
