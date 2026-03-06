from flask import Flask

from routes.items import items_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(items_bp, url_prefix="/items")

if __name__ == "__main__":
    app.run(debug=True)
