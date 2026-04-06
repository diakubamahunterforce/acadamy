from ..extensions import db

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    course_id = db.Column(db.Integer)
    status = db.Column(db.String(20), default="paid")
    progress = db.Column(db.Integer, default=0) 
