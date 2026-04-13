from ..extensions import db
from .course import Course
class Lesson(db.Model):
    __tablename__ = "lesson"
   
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    video_public_id = db.Column(db.String(255))
    video_url = db.Column(db.String(500))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    duration = db.Column(db.Integer)  # duração em segundos

