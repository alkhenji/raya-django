# Raya (راية) Platform

Raya is a platform that connects startups with investors in the MENA region. The platform is built with Django and supports both English and Arabic interfaces.

## Features

- Bilingual support (English/Arabic)
- Startup profiles and listings
- Investor profiles and listings
- Investment deal management
- User authentication and authorization
- Responsive design with Bootstrap 5
- RTL support for Arabic interface

## Tech Stack

- Python 3.8+
- Django 4.2+
- PostgreSQL
- Bootstrap 5.3
- Font Awesome 6.0

## File Structure

```
raya-django/
├── core/                   # Main application directory
│   ├── migrations/        # Database migrations
│   ├── templates/        # App-specific templates
│   │   └── core/        
│   ├── __init__.py
│   ├── admin.py          # Admin interface configuration
│   ├── apps.py          # App configuration
│   ├── forms.py         # Form definitions
│   ├── models.py        # Database models
│   ├── urls.py          # URL routing
│   └── views.py         # View logic
├── locale/               # Translation files
│   └── ar/              # Arabic translations
│       └── LC_MESSAGES/
│           └── django.po
├── static/              # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── img/
├── templates/           # Global templates
│   ├── base.html       # Base template
│   ├── home_ar.html    # Arabic homepage
│   └── home.html       # English homepage
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
└── raya/              # Project settings directory
    ├── __init__.py
    ├── settings.py    # Project settings
    ├── urls.py        # Project URL configuration
    └── wsgi.py        # WSGI configuration
```

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/raya-django.git
cd raya-django
```

2. Create and activate a virtual environment:
```bash
# On macOS/Linux
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root and add:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/raya
```

5. Set up the database:
```bash
# Create database
createdb raya

# Run migrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Compile translations:
```bash
python manage.py compilemessages
```

8. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Development

### Working with Translations

1. Extract messages for translation:
```bash
python manage.py makemessages -l ar
```

2. Edit translations in `locale/ar/LC_MESSAGES/django.po`

3. Compile translations:
```bash
python manage.py compilemessages
```

### Database Updates

When making model changes:

1. Create migrations:
```bash
python manage.py makemigrations
```

2. Apply migrations:
```bash
python manage.py migrate
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.