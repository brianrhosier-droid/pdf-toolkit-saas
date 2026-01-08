# Quick Start Guide - Get Running in 5 Minutes

This guide will get your PDF Toolkit SaaS up and running as quickly as possible.

## Step 1: Install Python (if not already installed)

**Windows:**
1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. ✅ **IMPORTANT:** Check "Add Python to PATH" during installation
4. Click "Install Now"

**Mac:**
```bash
# Using Homebrew (recommended)
brew install python3
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
```

## Step 2: Run Setup

Open Terminal/Command Prompt and navigate to the project folder:

```bash
cd pdf-toolkit-saas
```

**On Windows:**
```bash
setup.bat
```

**On Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

This will install everything you need!

## Step 3: Start the Application

**On Windows:**
```bash
start.bat
```

**On Mac/Linux:**
```bash
chmod +x start.sh
./start.sh
```

## Step 4: Open Your Browser

Go to: **http://localhost:5000**

You should see your PDF Toolkit homepage!

## Step 5: Create an Account

1. Click "Sign Up"
2. Enter your email and password
3. You're in! You have 5 free operations to test with.

## Testing the Application

Try each tool:
1. **Merge PDFs:** Upload 2+ PDF files and combine them
2. **Split PDF:** Upload a PDF and split it into pages
3. **Compress PDF:** Upload a PDF to reduce its size
4. **Convert to PDF:** Upload images and convert to PDF

## Optional: Set Up Stripe Payments (For Real Money)

If you want to accept real payments:

1. **Create a Stripe account:**
   - Go to https://stripe.com and sign up
   - It's free to create an account

2. **Get your API keys:**
   - Go to https://dashboard.stripe.com/apikeys
   - Copy your "Publishable key" and "Secret key"

3. **Update your .env file:**
   - Open the file named `.env` in the pdf-toolkit-saas folder
   - Replace these lines with your actual keys:
     ```
     STRIPE_PUBLIC_KEY=pk_test_your_actual_key_here
     STRIPE_SECRET_KEY=sk_test_your_actual_key_here
     ```

4. **Create subscription products in Stripe:**
   - Go to https://dashboard.stripe.com/products
   - Click "Add Product"
   - Create "Basic Plan": $9/month, recurring
   - Create "Pro Plan": $29/month, recurring
   - Copy each Price ID and update in `.env`:
     ```
     STRIPE_PRICE_BASIC=price_xxxxx
     STRIPE_PRICE_PRO=price_xxxxx
     ```

5. **Restart the application:**
   - Press Ctrl+C to stop
   - Run `start.bat` (Windows) or `./start.sh` (Mac/Linux) again

Now you can test subscriptions! Use Stripe's test card numbers:
- Card: 4242 4242 4242 4242
- Expiry: Any future date
- CVC: Any 3 digits

## What's Next?

### To Run Locally and Test:
- You're all set! Keep the server running and use http://localhost:5000

### To Deploy and Make Real Money:
1. Read `DEPLOYMENT.md` for deployment instructions
2. Choose a hosting provider (DigitalOcean recommended)
3. Set up your domain name
4. Switch Stripe to live mode
5. Start marketing!

## Common Issues

### "Python not found"
- Make sure Python is installed and added to PATH
- Restart your terminal/command prompt after installing Python

### "pip not found"
- Python should come with pip
- Try: `python -m pip install -r requirements.txt`

### "Module not found" errors
- Make sure you ran setup.bat/setup.sh first
- Make sure you're running from the pdf-toolkit-saas directory

### Port 5000 already in use
- Another app is using port 5000
- Edit `app.py`, change the last line to use a different port:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)
  ```

### Can't access from other devices on network
- The app runs on `0.0.0.0` so it should be accessible
- Find your computer's IP address:
  - Windows: `ipconfig`
  - Mac/Linux: `ifconfig`
- Access from other devices: `http://YOUR_IP:5000`

## How to Stop the Server

Press `Ctrl+C` in the terminal where it's running.

## How to Restart

Just run `start.bat` (Windows) or `./start.sh` (Mac/Linux) again!

## File Structure

```
pdf-toolkit-saas/
├── start.bat / start.sh    ← Run this to start
├── setup.bat / setup.sh    ← Run this first (one time)
├── .env                    ← Your configuration (Stripe keys, etc.)
├── app.py                  ← Main application
├── README.md              ← Full documentation
├── DEPLOYMENT.md          ← How to deploy for real
└── templates/             ← Web pages
```

## Getting Help

1. Check the error message - it usually tells you what's wrong
2. Read the `README.md` for more detailed information
3. Check `DEPLOYMENT.md` for production deployment help

## Success Metrics

You'll know everything is working when:
- ✅ You can access http://localhost:5000
- ✅ You can create an account
- ✅ You can upload and merge PDFs
- ✅ The files download correctly
- ✅ (Optional) You can subscribe to a plan

## Ready to Make Money?

Once you've tested locally:
1. Deploy to DigitalOcean/Heroku (see DEPLOYMENT.md)
2. Set up your domain
3. Switch Stripe to live mode
4. Start marketing!

With ~53 customers at $19/month average, you'll hit $1000/month revenue!

---

**You're ready to go! Run `start.bat` or `./start.sh` and visit http://localhost:5000**
