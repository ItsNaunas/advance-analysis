"""
Script to create admin user
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.password_hasher import hash_password

def create_admin():
    """Create admin user"""
    app = create_app('development')
    
    with app.app_context():
        # Check if admin already exists
        user_repo = UserRepository()
        admin = user_repo.get_by_username('admin')
        
        if admin:
            print("Admin user already exists!")
            return
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@ffsmart.com',
            password_hash=hash_password('password'),
            role=User.ROLE_ADMIN
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: password")

if __name__ == '__main__':
    create_admin()
