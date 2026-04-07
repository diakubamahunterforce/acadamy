from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

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
    cloud_name="root",
    api_key="692675614742393",
    api_secret="3pAPhPL9DlnB6792Fs2LU3Aqu8s"
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
    if User.role not  in ["admin", "instructor"]:
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



@course_bp.route("/lessons/<int:lesson_id>/stream", methods=["GET"])
@jwt_required()
def stream_video(lesson_id):
    """
    Obter vídeo de uma aula
    ---
    tags:
      - Lessons
    security:
      - Bearer: []
    parameters:
      - name: lesson_id
        in: path
        type: integer
        required: true
        description: ID da aula
    responses:
      200:
        description: URL do vídeo
        schema:
          type: object
          properties:
            video_url:
              type: string
      403:
        description: Sem acesso
      404:
        description: Aula não encontrada
    """

    user_id = get_jwt_identity()

    lesson = Lesson.query.get(lesson_id)

    if not lesson:
        return jsonify({"error": "Aula não encontrada"}), 404

    purchase = Purchase.query.filter_by(
        user_id=user_id,
        course_id=lesson.course_id,
        status="paid"
    ).first()

    if not purchase:
        return jsonify({"error": "Sem acesso"}), 403

    return jsonify({
        "video_url": lesson.video_url
    })












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