from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

app = Flask(__name__)

# Habilitar CORS para el frontend
CORS(app, resources={r"/api/*": {"origins": os.getenv("ALLOWED_ORIGINS","*")}})

# Ruta de prueba (para verificar que el backend funciona)
@app.get("/api/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("FLASK_RUN_PORT", 5000)))
