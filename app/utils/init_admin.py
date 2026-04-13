from app import db
from app.models import user
from  app.models.user import User

def create_default_admin():
    admin_email = "admin@email.com"

    existing_admin = User.query.filter_by(email=admin_email).first()

    if not existing_admin:
        admin = User(
            name="Root Admin",
            email=admin_email,
            role="admin"
        )

        admin.set_password("123456")

        db.session.add(admin)
        db.session.commit()

        print("Default admin created!")