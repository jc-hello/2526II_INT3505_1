from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

from auth import auth_bp
from routes.items import items_bp
from routes.system import system_bp

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "change-me-in-production"

CORS(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(items_bp, url_prefix="/items")
app.register_blueprint(system_bp, url_prefix="/system")

# Swagger UI — served at /docs, spec at /static/swagger.yaml
SWAGGER_URL = "/docs"
API_URL = "/static/swagger.yaml"
swaggerui_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Week4 OpenAPI Training API"},
)
app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    app.run(debug=True)
