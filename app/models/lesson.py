from ..extensions import db
from .course import Course
class Lesson(db.Model):
    __tablename__ = "lesson"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    video_url = db.Column(db.String(500), nullable=True)


    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id", name="fk_lesson_course"),
        nullable=False
    )
