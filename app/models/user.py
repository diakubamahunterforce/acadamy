from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.String(20), default="student")

    def set_password(self, p):
        self.password = generate_password_hash(p)

    def check_password(self, p):
        return check_password_hash(self.password, p)
