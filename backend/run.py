from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

def create_app():
    app = Flask(__name__)

    # CORS
    CORS(app, resources={r"/api/*": {"origins": os.getenv("ALLOWED_ORIGINS", "*")}})

    # Healthcheck
    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    # Registrar blueprints
    from routes.pdf_routes import pdf_bp
    app.register_blueprint(pdf_bp, url_prefix="/api/pdf")

    from routes.pdf_template import pdf_template_bp
    app.register_blueprint(pdf_template_bp, url_prefix="/api/pdf")


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=int(os.getenv("FLASK_RUN_PORT", 5001)))
