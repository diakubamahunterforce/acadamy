from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models.purchase import Purchase
from ..models.course import Course
from ..models.lesson import Lesson

course_my_bp = Blueprint("my_courses", __name__)


@course_my_bp.route("/my-courses", methods=["GET"])
@jwt_required()
def my_dashboard():
    """
    Meu Dashboard de Cursos
    ---
    tags:
      - Dashboard

    summary: Retorna cursos comprados pelo usuário logado

    description: |
      Este endpoint retorna todos os cursos comprados pelo usuário autenticado,
      incluindo progresso, número total de aulas e última aula disponível.

    security:
      - Bearer: []

    responses:
      200:
        description: Lista de cursos do usuário autenticado
        schema:
          type: object
          properties:
            user_id:
              type: integer
              example: 1
            total_courses:
              type: integer
              example: 3
            courses:
              type: array
              items:
                type: object
                properties:
                  purchase_id:
                    type: integer
                    example: 10
                  progress:
                    type: integer
                    example: 50
                  total_lessons:
                    type: integer
                    example: 20
                  status:
                    type: string
                    example: paid
                  course:
                    type: object
                    properties:
                      id:
                        type: integer
                        example: 5
                      title:
                        type: string
                        example: Python Avançado
                      description:
                        type: string
                        example: Curso completo de Python
                      price:
                        type: number
                        example: 29.99
                  last_lesson:
                    type: object
                    nullable: true
                    properties:
                      id:
                        type: integer
                        example: 12
                      title:
                        type: string
                        example: Introdução

      401:
        description: Token inválido ou não enviado
    """

    #  FIX: converter de volta para int
    user_id = int(get_jwt_identity())

    purchases = Purchase.query.filter_by(
        user_id=user_id,
        status="paid"
    ).all()

    result = []

    for p in purchases:
        course = Course.query.get(p.course_id)
        if not course:
            continue

        total_lessons = Lesson.query.filter_by(course_id=course.id).count()

        progress = int(p.progress or 0)

        last_lesson = Lesson.query.filter_by(course_id=course.id)\
            .order_by(Lesson.id.desc())\
            .first()

        result.append({
            "purchase_id": p.id,
            "progress": progress,
            "total_lessons": total_lessons,
            "status": p.status,
            "course": {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "price": course.price
            },
            "last_lesson": {
                "id": last_lesson.id,
                "title": last_lesson.title
            } if last_lesson else None
        })

    return jsonify({
        "user_id": user_id,
        "total_courses": len(result),
        "courses": result
    })