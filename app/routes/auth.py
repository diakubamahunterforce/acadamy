from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..models.user import User
from ..extensions import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
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
              example: João
            email:
              type: string
              example: joao@email.com
            password:
              type: string
              example: 123456
    responses:
      200:
        description: Usuário criado com sucesso
      400:
        description: Erro na criação
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "no data"}), 400

    user = User(name=data["name"], email=data["email"])
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "created"})



from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..models.user import User



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