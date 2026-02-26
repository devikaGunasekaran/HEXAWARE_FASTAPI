from sqlalchemy.orm import Session
from database.session import SessionLocal
from models import User, UserRole
from core.security import get_password_hash

def seed_data():
    db = SessionLocal()
    try:
        # Check if superadmin exists
        superadmin = db.query(User).filter(User.email == "admin@eams.com").first()
        if not superadmin:
            superadmin = User(
                name="Super Admin",
                email="admin@eams.com",
                password=get_password_hash("admin123"),
                role=UserRole.SUPERADMIN
            )
            db.add(superadmin)
            db.commit()
            print("SuperAdmin created: admin@eams.com / admin123")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
