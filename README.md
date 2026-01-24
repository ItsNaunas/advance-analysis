# FFSmart Smart Fridge Inventory Management System

A comprehensive inventory management system for commercial restaurant smart fridges, featuring automated tracking, notifications, and reordering capabilities.

## Features

- **User Authentication & Authorization**: Role-based access control (Head Chef, Chef, Delivery Person, Admin, Health & Safety Officer)
- **Inventory Management**: Real-time tracking of food items with expiration dates
- **Notifications & Alerts**: Automated warnings for expiring items and low stock
- **Automated Reordering**: Weekly reorder generation with Head Chef confirmation
- **Delivery Management**: Delivery person access and manifest matching
- **Audit Logging**: Complete audit trail of all system actions

## Technology Stack

- **Backend**: Python 3.10+ with Flask
- **Database**: SQLite
- **Frontend**: HTML/CSS/JavaScript with Jinja2 templates
- **Testing**: pytest

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. Create initial admin user:
```bash
python scripts/create_admin.py
```

6. Run the application:
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
ffsmart/
├── app/                    # Main application package
│   ├── models/            # Database models
│   ├── services/          # Business logic
│   ├── repositories/      # Data access layer
│   ├── controllers/       # Route handlers
│   ├── middleware/         # Auth and RBAC
│   ├── templates/         # Jinja2 templates
│   └── static/            # CSS, JS, images
├── tests/                 # Test files
├── docs/                  # Documentation
└── migrations/            # Database migrations
```

## Testing

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

## License

This project is part of COMP30121 - Advanced Analysis and Design coursework.
