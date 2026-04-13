from flask import Blueprint, jsonify,request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.purchase import Purchase,Course
import uuid
from ..extensions import db
from hashlib import sha256
import hmac
import hashlib

def generate_reference():
    return f"PUR-{uuid.uuid4().hex[:10].upper()}"

SECRET = "minha_chave_secreta_super_segura"

purchase_bp = Blueprint("payment", __name__)

@purchase_bp.route("/buy", methods=["POST"])
@jwt_required()
def buy_course():

    """
    Criar compra de curso

    ---
    tags:
      - Payments
    security:
      - Bearer: []

    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - course_id
          properties:
            course_id:
              type: integer
              example: 1

    responses:
      201:
        description: Compra criada com sucesso
      400:
        description: course_id obrigatório
      404:
        description: Curso não encontrado
    """
   


       



    user_id = get_jwt_identity()
    data = request.get_json()

    course_id = data.get("course_id")

    if not course_id:
        return jsonify({"error": "course_id obrigatório"}), 400

    # 🔥 AQUI É ONDE ENTRA O CÓDIGO
    existing = Purchase.query.filter_by(
        user_id=user_id,
        course_id=course_id
    ).first()

    if existing:
        return jsonify({"error": "Compra já existe"}), 409

    course = Course.query.get(course_id)

    if not course:
        return jsonify({"error": "curso não encontrado"}), 404

    purchase = Purchase(
        user_id=user_id,
        course_id=course.id,
        amount=course.price,
        reference=generate_reference(),
        status="pending"
    )

    db.session.add(purchase)
    db.session.commit()

    return jsonify({
        "message": "Compra criada com sucesso",
        "reference": purchase.reference,
        "amount": purchase.amount,
        "status": purchase.status
    }), 201





@purchase_bp.route("/webhook", methods=["POST"])
@jwt_required()  # opcional (se quiser proteger também por JWT)
def webhook():
    """
    Webhook de confirmação de pagamento

    ---
    tags:
      - Payments
    summary: Confirma pagamento via gateway

    security:
      - Bearer: []

    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - reference
            - status
          properties:
            reference:
              type: string
              example: PUR-A1B2C3D4E5
            status:
              type: string
              enum: [paid, failed]
              example: paid

    responses:
      200:
        description: Pagamento atualizado com sucesso
      400:
        description: Dados inválidos
      401:
        description: Não autorizado / assinatura inválida
      404:
        description: Compra não encontrada
    """

    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    reference = data.get("reference")
    status = data.get("status")

    if not reference or not status:
        return jsonify({"error": "reference e status são obrigatórios"}), 400

    purchase = Purchase.query.filter_by(reference=reference).first()

    if not purchase:
        return jsonify({"error": "compra não encontrada"}), 404

    if status == "paid":
        purchase.status = "paid"
    elif status == "failed":
        purchase.status = "failed"
    else:
        return jsonify({"error": "status inválido"}), 400

    db.session.commit()

    return jsonify({
        "message": "webhook processado com sucesso",
        "reference": reference,
        "status": purchase.status
    }), 200

  