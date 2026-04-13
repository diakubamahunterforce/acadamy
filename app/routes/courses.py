from flask import Blueprint, request, jsonify
from flask_jwt_extended import current_user, jwt_required, get_jwt_identity

from app.models.user import User
from ..models.course import Course
from ..models.lesson import Lesson
from ..models.purchase import Purchase
from ..extensions import db
import  cloudinary
import cloudinary.uploader

import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="dhpain7wq",
    api_key="772767193863469",
    api_secret="wJH5akhlGNv1Ltg-OURGSpTODTQ"
)


course_bp = Blueprint("course", __name__)


@course_bp.route("/courses", methods=["GET"])
@jwt_required()
def list_courses():
    """
    Listar cursos

    ---
    tags:
      - Courses
    security:
      - Bearer: []

    responses:
      200:
        description: Lista de cursos
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  title:
                    type: string
                    example: Python Básico
    """

    courses = Course.query.all()

    return jsonify([
        {
            "id": c.id,
            "title": c.title
        }
        for c in courses
    ]), 200


@course_bp.route("/lessons", methods=["POST"])
@jwt_required()
def create_lesson():
    """
    Criar aula com upload de vídeo
    ---
    tags:
      - Lessons
    security:
      - Bearer: []
    consumes:
      - multipart/form-data
    parameters:
      - name: title
        in: formData
        type: string
        required: true

      - name: course_id
        in: formData
        type: integer
        required: true

      - name: video
        in: formData
        type: file
        required: true

    responses:
      201:
        description: Aula criada com sucesso
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role not in ["admin", "instructor"]:
        return jsonify({"error": "Acesso negado"}), 403


    title = request.form.get("title")
    course_id = request.form.get("course_id")
    file = request.files.get("video")

    if not title or not course_id or not file:
        return jsonify({"error": "Dados incompletos"}), 400

    import cloudinary.uploader

    result = cloudinary.uploader.upload(
        file,
        resource_type="video"
    )

    video_url = result.get("secure_url")

    lesson = Lesson(
        title=title,
        course_id=course_id,
        video_url=video_url
    )

    db.session.add(lesson)
    db.session.commit()

    return jsonify({
        "message": "Aula criada com sucesso",
        "lesson_id": lesson.id,
        "video_url": video_url
    }), 201



@course_bp.route("/courses/<int:course_id>/lessons", methods=["GET"])
@jwt_required()
def get_course_lessons(course_id):
    """
    Obter todas as aulas de um curso (com verificação de acesso)
    ---
    tags:
      - Courses
    security:
      - Bearer: []

    parameters:
      - name: course_id
        in: path
        type: integer
        required: true
        description: ID do curso

    responses:
      200:
        description: Lista de aulas do curso
        schema:
          type: object
          properties:
            course_id:
              type: integer
            lessons:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  title:
                    type: string
                  video_url:
                    type: string

      403:
        description: Sem acesso ao curso

      404:
        description: Curso não encontrado ou sem aulas
    """

    user_id = get_jwt_identity()

    purchase = Purchase.query.filter_by(
        user_id=user_id,
        course_id=course_id,
        status="paid"
    ).first()

    if not purchase:
        return jsonify({"error": "Sem acesso ao curso"}), 403

    lessons = Lesson.query.filter_by(course_id=course_id).all()

    if not lessons:
        return jsonify({"error": "Curso não encontrado ou sem aulas"}), 404

    return jsonify({
        "course_id": course_id,
        "lessons": [
            {
                "id": l.id,
                "title": l.title,
                "video_url": f"/lessons/{l.id}/stream"
            }
            for l in lessons
        ]
    }), 200










@course_bp.route("/courses/<int:course_id>/lessons", methods=["GET"])
@jwt_required()
def get_lessons(course_id):
    """
    Listar aulas de um curso
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
        description: ID do curso
    responses:
      200:
        description: Lista de aulas
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              video_url:
                type: string
      403:
        description: Sem acesso ao curso
    """

    user_id = get_jwt_identity()

    purchase = Purchase.query.filter_by(
        user_id=user_id,
        course_id=course_id,
        status="paid"
    ).first()

    if not purchase:
        return jsonify({"error": "Sem acesso"}), 403

    lessons = Lesson.query.filter_by(course_id=course_id).all()

    return jsonify([
        {
            "id": l.id,
            "title": l.title,
            "video_url": f"/lessons/{l.id}/stream"
        }
        for l in lessons
    ]), 200