#!/usr/bin/env python
"""
Deployment Checklist Script
---------------------------
Run this script before deploying to verify your Django project is ready for production.
"""

import os
import sys
import subprocess
import re
from pathlib import Path

# Add the project to the Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Try to load Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pinakAndDjango.settings')

try:
    from django.conf import settings
except ImportError:
    print("❌ Could not import Django settings. Is Django installed?")
    sys.exit(1)

# Load dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
    print("✅ Environment variables loaded from .env file")
except (ImportError, FileNotFoundError):
    print("⚠️ No .env file found or python-dotenv not installed")

def check_debug_mode():
    """Check if DEBUG is set to False for production."""
    if settings.DEBUG:
        print("❌ DEBUG is set to True. Set DEBUG=False for production.")
    else:
        print("✅ DEBUG is set to False")

def check_secret_key():
    """Check if SECRET_KEY is properly configured."""
    if settings.SECRET_KEY == 'django-insecure-g5titoer-5mjr-4ev2_ey#9r3&8!p4%8dy4#0!4^g3$j93%nfq':
        print("❌ Using insecure default SECRET_KEY. Set a proper SECRET_KEY for production.")
    elif os.environ.get('DJANGO_SECRET_KEY'):
        print("✅ SECRET_KEY is set via environment variable")
    else:
        print("✅ SECRET_KEY is configured")

def check_allowed_hosts():
    """Check if ALLOWED_HOSTS is properly configured."""
    if not settings.ALLOWED_HOSTS or settings.ALLOWED_HOSTS == ['localhost', '127.0.0.1']:
        print("❌ ALLOWED_HOSTS is not configured for production.")
    else:
        print(f"✅ ALLOWED_HOSTS is configured: {', '.join(settings.ALLOWED_HOSTS)}")

def check_database():
    """Check if database is properly configured."""
    if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3' and not settings.DEBUG:
        print("⚠️ Using SQLite in production is not recommended. Consider using PostgreSQL.")
    else:
        print("✅ Database configuration looks good")

def check_static_files():
    """Check if static files configuration is correct."""
    if not os.path.exists(settings.STATIC_ROOT):
        print(f"❌ STATIC_ROOT directory doesn't exist: {settings.STATIC_ROOT}")
        print("   Run 'python manage.py collectstatic' before deployment")
    else:
        print("✅ STATIC_ROOT directory exists")
    
    if 'whitenoise.middleware.WhiteNoiseMiddleware' not in settings.MIDDLEWARE:
        print("❌ WhiteNoise middleware is not enabled for static files serving")
    else:
        print("✅ WhiteNoise middleware is enabled")

def check_security_middleware():
    """Check if security middleware is properly configured."""
    security_middleware = 'django.middleware.security.SecurityMiddleware'
    if security_middleware not in settings.MIDDLEWARE:
        print("❌ Security middleware is not enabled")
    else:
        print("✅ Security middleware is enabled")

def check_ssl_settings():
    """Check if SSL settings are properly configured."""
    if not settings.DEBUG:
        if not getattr(settings, 'SECURE_SSL_REDIRECT', False):
            print("⚠️ SECURE_SSL_REDIRECT is not enabled")
        else:
            print("✅ SECURE_SSL_REDIRECT is enabled")
        
        if not getattr(settings, 'SESSION_COOKIE_SECURE', False):
            print("⚠️ SESSION_COOKIE_SECURE is not enabled")
        else:
            print("✅ SESSION_COOKIE_SECURE is enabled")
        
        if not getattr(settings, 'CSRF_COOKIE_SECURE', False):
            print("⚠️ CSRF_COOKIE_SECURE is not enabled")
        else:
            print("✅ CSRF_COOKIE_SECURE is enabled")

def check_requirements():
    """Check if all required packages are installed."""
    try:
        with open(BASE_DIR / 'requirements.txt', 'r') as f:
            requirements = f.read()
        
        print("✅ requirements.txt file exists")
        
        # Check for important packages
        if 'gunicorn' not in requirements:
            print("❌ gunicorn is not in requirements.txt")
        if 'whitenoise' not in requirements:
            print("❌ whitenoise is not in requirements.txt")
        if 'python-dotenv' not in requirements:
            print("❌ python-dotenv is not in requirements.txt")
    except FileNotFoundError:
        print("❌ requirements.txt file not found")

def check_procfile():
    """Check if Procfile exists for Heroku deployment."""
    if os.path.exists(BASE_DIR / 'Procfile'):
        print("✅ Procfile exists")
    else:
        print("⚠️ Procfile not found (only needed for Heroku deployment)")

def check_runtime():
    """Check if runtime.txt exists for Heroku deployment."""
    if os.path.exists(BASE_DIR / 'runtime.txt'):
        with open(BASE_DIR / 'runtime.txt', 'r') as f:
            runtime = f.read().strip()
        print(f"✅ runtime.txt exists with Python version: {runtime}")
    else:
        print("⚠️ runtime.txt not found (only needed for Heroku deployment)")

def check_tailwind():
    """Check if Tailwind CSS is properly built for production."""
    if 'tailwind' in settings.INSTALLED_APPS:
        theme_app = getattr(settings, 'TAILWIND_APP_NAME', 'theme')
        css_path = BASE_DIR / theme_app / 'static' / theme_app / 'css' / 'dist' / 'styles.css'
        if not os.path.exists(css_path):
            print("❌ Tailwind CSS not built. Run 'python manage.py tailwind build'")
        else:
            print("✅ Tailwind CSS is built")
    else:
        print("ℹ️ Tailwind CSS is not used in this project")

def main():
    print("\n=== Django Deployment Checklist ===\n")
    
    check_debug_mode()
    check_secret_key()
    check_allowed_hosts()
    check_database()
    check_static_files()
    check_security_middleware()
    check_ssl_settings()
    check_requirements()
    check_procfile()
    check_runtime()
    check_tailwind()
    
    print("\n=== Checklist Complete ===")
    print("\nRemember to:")
    print("1. Run 'python manage.py check --deploy' for Django's built-in deployment checks")
    print("2. Make sure your database is properly backed up before deployment")
    print("3. Test your application thoroughly in a staging environment first")
    
if __name__ == "__main__":
    main() 