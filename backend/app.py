from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lostfound.db"
app.config["JWT_SECRET_KEY"] = "your-secret-key"
app.config["CORS_HEADERS"] = "Content-Type"

db.init_app(app)
CORS(app)
JWTManager(app)

from routes.auth import auth_bp
from routes.items import items_bp
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(items_bp, url_prefix="/api/items")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)