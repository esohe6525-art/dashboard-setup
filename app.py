from flask import Flask
from routes import auth_bp, main_bp

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "dev-secret-key"
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix="/auth")


if __name__ == "__main__":
    app.run(debug=True)
