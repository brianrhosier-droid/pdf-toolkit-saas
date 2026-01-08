import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///pdftoolkit.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Stripe
    STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
    STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')
    STRIPE_PRICE_BASIC = os.getenv('STRIPE_PRICE_BASIC', '')
    STRIPE_PRICE_PRO = os.getenv('STRIPE_PRICE_PRO', '')

    # Usage Limits
    FREE_TIER_LIMIT = int(os.getenv('FREE_TIER_LIMIT', 5))
    BASIC_TIER_LIMIT = int(os.getenv('BASIC_TIER_LIMIT', 100))
    PRO_TIER_LIMIT = int(os.getenv('PRO_TIER_LIMIT', 1000))

    # File Upload
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 10))
    MAX_CONTENT_LENGTH = MAX_FILE_SIZE_MB * 1024 * 1024
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
