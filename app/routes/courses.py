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
        description: Lista de cursos   (apenas para usuários logados)
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
            "title": c.title,
             "description":c.description,
             "price":c.price,
         


        }
        for c in courses
    ]), 200








@course_bp.route("/courses/create", methods=["POST"])
@jwt_required()
def Create_course():
    """
    Criar um novo curso  (apenas admin/instructor)
    ---
    tags:
      - Courses
    security:
      - Bearer: []

    consumes:
      - application/json

    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - title
          properties:
            title:
              type: string
              example: "Curso de Python"
            description:
              type: string
              example: "Aprenda Python do zero ao avançado"
            price:
              type: number
              example: 49.99

    responses:
      201:
        description: Curso criado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
            course:
              type: object
              properties:
                id:
                  type: integer
                title:
                  type: string

      400:
        description: Erro nos dados enviados

      401:
        description: Não autorizado (token inválido)
    """
    
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role not in ["admin", "instructor"]:
        return jsonify({"error": "Acesso negado"}), 403

    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    price = data.get("price")

    if not title:
        return jsonify({"error": "Título é obrigatório"}), 400

    course = Course(
        title=title,
        description=description,
        price=price
    )

    db.session.add(course)
    db.session.commit()

    return jsonify({
        "message": "Curso criado com sucesso",
        "course": {
            "id": course.id,
            "title": course.title
        }
    }), 201

















@course_bp.route("/lessons/create-video", methods=["POST"])
@jwt_required()
def create_lesson_video():
    """
    Criar aula com upload de vídeo (Cloudinary)
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
        schema:
          type: object
          properties:
            message:
              type: string
              example: Aula criada com sucesso

            lesson_id:
              type: integer
              example: 1

            public_id:
              type: string
              example: lessons/python_intro

            duration:
              type: integer
              example: 3600   #

      400:
        description: Dados incompletos

      403:
        description: Acesso negado
    """

    current_user = User.query.get(get_jwt_identity())

    if not current_user or current_user.role not in ["admin", "instructor"]:
        return jsonify({"error": "Acesso negado"}), 403

    title = request.form.get("title")
    course_id = request.form.get("course_id")
    file = request.files.get("video")

    if not title or not course_id or not file:
        return jsonify({"error": "Dados incompletos"}), 400

    result = cloudinary.uploader.upload(
        file,
        resource_type="video",
        folder="lessons"
    )

    lesson = Lesson(
        title=title,
        course_id=course_id,
        video_public_id=result.get("public_id"),
        duration=result.get("duration")
    )

    db.session.add(lesson)
    db.session.commit()

    return jsonify({
        "message": "Aula criada com sucesso",
        "lesson_id": lesson.id,
        "public_id": lesson.video_public_id,
        "duration": lesson.duration
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










@course_bp.route("/courses/<int:course_id>/stream", methods=["GET"])
@jwt_required()
def stream_course(course_id):
    """
    Stream de vídeo do curso (com verificação de pagamento)
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
        description: Stream autorizado com sucesso
        schema:
          type: object
          properties:
            course_id:
              type: integer
              example: 1

            lesson_id:
              type: integer
              example: 10

            stream_url:
              type: string
              example: https://res.cloudinary.com/demo/video/upload/sp_auto/video.m3u8

      403:
        description: Acesso negado (curso não pago)
        schema:
          type: object
          properties:
            error:
              type: string
              example: Curso não pago ou acesso negado

      404:
        description: Curso ou aula não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
              example: Sem aulas disponíveis

      401:
        description: Não autenticado (token inválido ou ausente)
    """

    user_id = get_jwt_identity()

    # 🔐 VERIFICAR PAGAMENTO
    purchase = Purchase.query.filter_by(
        user_id=user_id,
        course_id=course_id,
        status="paid"
    ).first()

    if not purchase:
        return jsonify({
            "error": "Curso não pago ou acesso negado"
        }), 403

    # 🎥 BUSCAR AULA
    lesson = Lesson.query.filter_by(course_id=course_id)\
        .order_by(Lesson.id.desc())\
        .first()

    if not lesson:
        return jsonify({"error": "Sem aulas disponíveis"}), 404

    # 🎬 GERAR STREAM HLS
    stream_url = cloudinary.CloudinaryVideo(
        lesson.video_public_id
    ).build_url(
        secure=True,
        format="m3u8",
        resource_type="video"
    )

    return jsonify({
        "course_id": course_id,
        "lesson_id": lesson.id,
        "stream_url": stream_url
    }), 200






@course_bp.route("/lessons/<int:lesson_id>/stream", methods=["GET"])
@jwt_required(optional=True)
def stream_lesson(lesson_id):
    """
    Stream de vídeo da aula (HLS / Cloudinary)
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
        description: Link de streaming gerado com sucesso
        schema:
          type: object
          properties:
            lesson_id:
              type: integer
              example: 1

            title:
              type: string
              example: Introdução ao Python

            stream_url:
              type: string
              example: https://res.cloudinary.com/demo/video/upload/sp_auto/lesson.m3u8

      404:
        description: Aula ou vídeo não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: Vídeo não encontrado

      401:
        description: Não autenticado

      403:
        description: Acesso negado
    """

    lesson = Lesson.query.get_or_404(lesson_id)

    if not lesson.video_public_id:
        return jsonify({"error": "Vídeo não encontrado"}), 404

    stream_url = cloudinary.CloudinaryVideo(
        lesson.video_public_id
    ).build_url(
        secure=True,
        format="m3u8",
        resource_type="video" \
    
    )

    return jsonify({
        "lesson_id": lesson.id,
        "title": lesson.title,
        "stream_url": stream_url
    }), 200