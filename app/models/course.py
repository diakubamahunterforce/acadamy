from ..extensions import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
   
    course_id = db.Column(
    db.Integer,
    db.ForeignKey("course.id", name="fk_course_course_id", ondelete="CASCADE"),
    nullable=False
)