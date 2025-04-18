# Learning Platform - Django & Tailwind CSS

A modern learning platform built with Django and Tailwind CSS.

## Features

- Course catalog with filtering and search
- Detailed course pages with reviews
- Shopping cart functionality
- Responsive design
- Mobile-friendly navigation
- Page loading animations

## Local Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Start the development server: `python manage.py runserver`

## Deployment Guide

This project is configured to be deployed to various hosting services. Follow these instructions to deploy successfully.

### Prerequisites

- Python 3.11 or later
- PostgreSQL (for production)
- Node.js and npm (for Tailwind CSS)

### Preparing for Deployment

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd pinakAndDjango
   ```

2. **Set up environment variables**:
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit the `.env` file and update all values with your actual configuration

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Compile static files**:
   ```bash
   python manage.py collectstatic
   ```

5. **Build Tailwind CSS**:
   ```bash
   python manage.py tailwind build
   ```

### Deployment Options

#### Option 1: Render

1. Create a new Web Service
2. Connect your GitHub repository
3. Use the following settings:
   - **Build Command**: `python -m pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py tailwind build`
   - **Start Command**: `gunicorn pinakAndDjango.wsgi:application`
4. Add the environment variables from your `.env` file
5. Deploy

#### Option 2: Heroku

1. Install Heroku CLI and login:
   ```bash
   heroku login
   ```

2. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

3. Add Heroku PostgreSQL:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. Configure environment variables:
   ```bash
   heroku config:set DJANGO_SECRET_KEY=your-secret-key
   heroku config:set DJANGO_DEBUG=False
   # Set other variables from .env
   ```

5. Deploy to Heroku:
   ```bash
   git push heroku main
   ```

6. Run migrations:
   ```bash
   heroku run python manage.py migrate
   ```

#### Option 3: PythonAnywhere

1. Create a PythonAnywhere account
2. Create a new web app with manual configuration (Python)
3. Set up a virtualenv and install requirements
4. Configure the WSGI file to point to your Django project
5. Create a PostgreSQL database
6. Set environment variables in the virtual environment's activation script
7. Collect static files and set up static files serving

### Post-Deployment Steps

1. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

2. **Create a superuser** (if needed):
   ```bash
   python manage.py createsuperuser
   ```

3. **Configure a domain name** (optional but recommended)

4. **Set up SSL** (most platforms handle this automatically)

### Troubleshooting

- **Static files not loading**: Check `STATIC_ROOT` and `STATICFILES_DIRS` settings
- **Database connection issues**: Verify your `DATABASE_URL` is correct
- **500 errors**: Check the server logs for detailed error messages

For more information, consult the [Django deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/).

## Important Deployment Steps

Before deploying to production:

1. Set `DEBUG=False` in environment variables
2. Generate a new secret key and set it as `DJANGO_SECRET_KEY`
3. Run `python manage.py collectstatic`
4. Update `ALLOWED_HOSTS` in settings.py if needed
5. Use PostgreSQL for production (already configured in settings)
6. Make sure media files are properly handled

## Database Migrations

When deploying with a PostgreSQL database:

```bash
python manage.py migrate
```

## Adding Initial Data

You can create fixtures for initial data:

```bash
python manage.py dumpdata learning --indent 2 > learning/fixtures/initial_data.json
```

And load them on the production server:

```bash
python manage.py loaddata learning/fixtures/initial_data.json
``` 