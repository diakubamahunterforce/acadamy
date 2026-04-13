from ..extensions import db
from datetime import datetime
from ..extensions import db
from .course import Course
from .user import User
from .lesson import Lesson


class Purchase(db.Model):
    __tablename__ = "purchases"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)

    # pagamento
    status = db.Column(db.String(20), default="pending")  
    # pending | paid | failed

    transaction_id = db.Column(db.String(255), nullable=True)

    amount = db.Column(db.Float, nullable=False)

    # progresso do curso
    progress = db.Column(db.Integer, default=0)
    reference=db.Column(db.String(20), unique=True, nullable=False)

    # datas
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # evitar duplicação
    __table_args__ = (
        db.UniqueConstraint('user_id', 'course_id', name='unique_user_course'),
    )