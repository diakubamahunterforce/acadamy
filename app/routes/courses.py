from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.course import Course
from ..models.lesson import Lesson
from ..models.purchase import Purchase
from ..extensions import db

course_bp = Blueprint("course", __name__)


@course_bp.route("/courses", methods=["GET"])
@jwt_required()
def list_courses():
    """
    Listar cursos

  
    ---
    tags:
      security:
        - Bearer: []
      
    responses:
      200:
        description: Lista de cursos
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
    """
    courses = Course.query.all()
    return jsonify([{"id": c.id, "title": c.title} for c in courses])


@course_bp.route("/courses", methods=["POST"])
@jwt_required()
def create_course():
    """
    Criar curso
    ---
    tags:
    security:
      - Bearer: []
      - Courses
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - title
            - description
            - price
          properties:
            title:
              type: string
            description:
              type: string
            price:
              type: number
    responses:
      200:
        description: Curso criado com sucesso
    """
    data = request.json

    c = Course(
        title=data["title"],
        description=data["description"],
        price=data["price"]
    )
    db.session.add(c)
    db.session.commit()

    return jsonify({"message": "created"})


@course_bp.route("/courses/<int:course_id>/lessons", methods=["GET"])
@jwt_required()
def get_lessons(course_id):
    """
    Listar aulas de um curso (com autenticação)
    ---
    tags:
      - Lessons
    security:
       - Bearer: []
    parameters:
      - name: course_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Lista de aulas
      403:
        description: Sem acesso ao curso
    """
    user = get_jwt_identity()

    access = Purchase.query.filter_by(
        user_id=user,
        course_id=course_id,
        status="paid"
    ).first()

    if not access:
        return jsonify({"error": "no access"}), 403

    lessons = Lesson.query.filter_by(course_id=course_id).all()
 
  

    return jsonify([
        {"id": l.id, "title": l.title, "video_url": l.video_url}
        for l in lessons
    ])