import hashlib

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash

from app.utils.email import send_email
from ..models.user import User
from ..extensions import db
import random
import time
reset_codes = {}
auth_bp = Blueprint("auth", __name__)




@auth_bp.route("/register/student", methods=["POST"])
def register():
    """
    Registro de usuário
    ---
    tags:
      - Auth
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - password
          properties:
            name:
              type: string
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Usuário criado com sucesso
      400:
        description: Erro na criação
    """

    data = request.get_json()

    if not data:
        return jsonify({"error": "no data"}), 400

    #  verificar campos
    if not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "dados obrigatórios"}), 400

    #  verificar se email já existe
    existing_user = User.query.filter_by(email=data["email"]).first()

    if existing_user:
        return jsonify({"error": "email já existe"}), 409


    user = User(
        name=data["name"],
        email=data["email"]
    )

    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "created"}), 201



@auth_bp.route("/register/instructor", methods=["POST"])
def register_instructor():
    """
    Registro de instrutor
    ---
    tags:
      - Auth
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - password
          properties:
            name:
              type: string
              example: João Professor
            email:
              type: string
              example: prof@email.com
            password:
              type: string
              example: 123456
    responses:
      201:
        description: Instrutor criado com sucesso
      400:
        description: Erro na criação
    """

    data = request.get_json()

    if not data:
        return jsonify({"error": "no data"}), 400

    
    if not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "dados obrigatórios"}), 400

    
    existing_user = User.query.filter_by(email=data["email"]).first()

    if existing_user:
        return jsonify({"error": "email já existe"}), 409

    # criar instrutor
    user = User(
        name=data["name"],
        email=data["email"],
        role="instructor"  
    )

    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "instructor created",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 201




























@auth_bp.route("/register/admin", methods=["POST"])
@jwt_required()

def register_admin():
    """
    Criar admin (somente admin pode criar outro admin)
    ---
    tags:
      - Auth
    security:
      - Bearer: []

    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - password
          properties:
            name:
              type: string
              example: Root Admin
            email:
              type: string
              example: admin@email.com
            password:
              type: string
              example: "123456"

    responses:
      201:
        description: Admin criado com sucesso
      400:
        description: Dados inválidos
      403:
        description: Sem permissão
      409:
        description: Email já existe
    """

    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    # verificar se está logado
    if not current_user:
        return jsonify({"error": "invalid token"}), 401

    # verificar role
    if current_user.role != "admin":
        return jsonify({"error": "not allowed"}), 403

    data = request.get_json()

    if not data:
        return jsonify({"error": "no data"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "missing fields"}), 400

    # verificar email existente
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"error": "email already exists"}), 409

    # criar admin
    user = User(
        name=name,
        email=email,
        role="admin"
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "admin created",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 201









@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login de usuário
    ---
    tags:
      - Auth

    summary: Autentica usuário e retorna JWT

    description: |
      Endpoint responsável por autenticar o usuário usando email e senha.
      Retorna um token JWT contendo o ID do usuário e sua role.

    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: joao@email.com
            password:
              type: string
              example: 123456

    responses:
      200:
        description: Login realizado com sucesso
        schema:
          type: object
          properties:
            token:
              type: string
              example: eyJhbGciOiJIUzI1NiIsInR5cCI6...
            user:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                email:
                  type: string
                  example: joao@email.com
                role:
                  type: string
                  example: student

      400:
        description: Dados inválidos

      401:
        description: Credenciais inválidas
    """


    data = request.get_json()

    if not data:
        return jsonify({"error": "no data provided"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password required"}), 400

   
    user = User.query.filter_by(email=email).first()


    if not user or not user.check_password(password):
        return jsonify({"error": "invalid credentials"}), 401

   
    token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )

  
    return jsonify({
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    }), 200











@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Enviar código OTP para recuperação de senha
    ---
    tags:
      - Auth
    description: Envia código de recuperação para o email (sem revelar se o usuário existe)
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
        description: Código enviado (resposta genérica por segurança)
      400:
        description: Email inválido
    """

    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email obrigatório"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "Se o email existir, o código foi enviado"}), 200

    code = str(random.randint(100000, 999999))
    hashed_code = hashlib.sha256(code.encode()).hexdigest()

    reset_codes[email] = {
        "code": hashed_code,
        "expire": time.time() + 600,
        "attempts": 0
    }

    send_email(
        to=email,
        subject="Recuperação de senha",
        body=f"Seu código é: {code}"
    )

    return jsonify({"message": "Se o email existir, o código foi enviado"})


















@auth_bp.route('/verify-code', methods=['POST'])
def verify_code():
    """
    Verificar código OTP
    ---
    tags:
      - Auth
    description: Valida o código enviado ao email (com limite de tentativas)
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - code
          properties:
            email:
              type: string
              example: user@gmail.com
            code:
              type: string
              example: "123456"
    responses:
      200:
        description: Código válido
      400:
        description: Código inválido ou expirado
      429:
        description: Muitas tentativas
    """

    data = request.json
    email = data.get("email")
    code = data.get("code")

    stored = reset_codes.get(email)

    if not stored:
        return jsonify({"error": "Código inválido"}), 400

    if stored["attempts"] >= 3:
        return jsonify({"error": "Muitas tentativas"}), 429

    hashed_code = hashlib.sha256(code.encode()).hexdigest()

    if time.time() > stored["expire"]:
        return jsonify({"error": "Código expirado"}), 400

    if stored["code"] != hashed_code:
        stored["attempts"] += 1
        return jsonify({"error": "Código inválido"}), 400

    return jsonify({"message": "Código válido"})

















@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Resetar senha do usuário
    ---
    tags:
      - Auth
    description: Atualiza a senha do usuário após validação do código OTP
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - code
            - password
          properties:
            email:
              type: string
              example: user@gmail.com
            code:
              type: string
              example: "123456"
            password:
              type: string
              example: "NovaSenha123"
    responses:
      200:
        description: Senha atualizada com sucesso
      400:
        description: Código inválido ou expirado
      404:
        description: Usuário não encontrado
    """

    data = request.json

    email = data.get("email")
    code = data.get("code")
    new_password = data.get("password")

    if not email or not code or not new_password:
        return jsonify({"error": "Dados incompletos"}), 400

    stored = reset_codes.get(email)

    if not stored:
        return jsonify({"error": "Código inválido"}), 400

    import hashlib, time
    hashed_code = hashlib.sha256(code.encode()).hexdigest()

    # verificar código
    if stored["code"] != hashed_code:
        return jsonify({"error": "Código inválido"}), 400

    # verificar expiração
    if time.time() > stored["expire"]:
        return jsonify({"error": "Código expirado"}), 400

    # buscar usuário
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    from werkzeug.security import generate_password_hash

    # atualizar senha
    user.password = generate_password_hash(new_password)
    db.session.commit()

    # apagar código após uso
    del reset_codes[email]

    return jsonify({"message": "Senha atualizada com sucesso"})