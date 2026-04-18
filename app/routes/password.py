from  flask import Blueprint, request, jsonify
from ..models.user import User
import random
from  utils.email import send_email 
import time
auth_bp = Blueprint('auth', __name__)
reset_codes = {}



@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Esqueci a senha (envio de código OTP)
    ---
    tags:
      - Auth
    description: Envia um código de recuperação para o email do usuário
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
          properties:
            email:
              type: string
              example: user@gmail.com
    responses:
      200:
        description: Código enviado com sucesso
      400:
        description: Email obrigatório
      404:
        description: Usuário não encontrado
    """

    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email obrigatório"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    code = str(random.randint(100000, 999999))

    reset_codes[email] = {
        "code": code,
        "expire": time.time() + 600
    }

    send_email(
        to=email,
        subject="Recuperação de senha",
        body=f"Seu código é: {code} (válido por 10 minutos)"
    )

    return jsonify({"message": "Código enviado para o email"})