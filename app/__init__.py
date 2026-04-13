from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from datetime import timedelta
from .extensions import db, jwt
from  flask_migrate import Migrate
from .routes.auth import auth_bp
from .routes.courses import course_bp
from .routes.purchase import purchase_bp
from .routes.my_curse import course_my_bp
from .utils.init_admin import create_default_admin

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
   
   
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

  
    app.config["JWT_SECRET_KEY"] = "C!8xQ2vR9mT#7pL6zK1yA4nF5dH3sW0bJ"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"

    jwt.init_app(app)

 

 
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Course API",
            "version": "1.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Escreve: Bearer <TOKEN>"
            }
        }
    }

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs"
    }

   
    Swagger(app, config=swagger_config, template=swagger_template)

 
    db.init_app(app)
    migrate = Migrate(app, db)

   
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(course_bp, url_prefix="/api")
    app.register_blueprint(purchase_bp, url_prefix="/api")
    app.register_blueprint(course_my_bp, url_prefix="/api")

    # ======================
    # CREATE TABLES
    # ======================
    with app.app_context():
        db.create_all()
        create_default_admin()

    return app