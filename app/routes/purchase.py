from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.purchase import Purchase
from ..extensions import db

purchase_bp = Blueprint("purchase", __name__)


@purchase_bp.route("/buy/<int:course_id>", methods=["POST"])
@jwt_required()
def buy(course_id):

    # 🔥 FIX AQUI
    user_id = int(get_jwt_identity())

    # evita compra duplicada
    existing = Purchase.query.filter_by(
        user_id=user_id,
        course_id=course_id
    ).first()

    if existing:
        return jsonify({"error": "already purchased"}), 400

    # cria compra
    p = Purchase(
        user_id=user_id,
        course_id=course_id,
        status="paid"
    )

    db.session.add(p)
    db.session.commit()

    return jsonify({
        "message": "bought",
        "course_id": course_id,
        "user_id": user_id
    }), 200