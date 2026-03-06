from flask import Flask
from flask_jwt_extended import JWTManager

from auth import auth_bp
from routes.items import items_bp

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "change-me-in-production"

jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(items_bp, url_prefix="/items")

if __name__ == "__main__":
    app.run(debug=True)
