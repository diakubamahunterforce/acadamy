from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import generate_password_hash
from ..models.user import User
from ..extensions import db

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
              example: 123456

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