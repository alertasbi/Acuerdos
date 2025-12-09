import os
import pyodbc
from flask import Flask, Blueprint, request, jsonify
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()
login_bp = Blueprint('login', __name__)
permisos_bp = Blueprint('permisos', __name__)

# Usando componentes de conexión separados
server = os.getenv("DB_HOST")
database = os.getenv("DB_DATABASE")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")

# Construye la cadena de conexión
conn_str = (
    f'DRIVER={{SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
)

#@login_bp.route('/api/login', methods=['GET'])
@login_bp.get('/login')
def login():
    try:
        user = request.args.get("user")
        password = request.args.get("password")

        if not user or not password:
            return jsonify({"error": "Missing user or password"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC spValidarUsuarioTest @strUsuario = ?, @strPassword = ?", (user, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return jsonify([{
                "message": "Login successful",
                "idUser": user[0],
                "name": user[1],
                "idRole": user[2],
                "role": user[3]
            }]), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@permisos_bp.get('/permisos')
def permisos():
    try:
        perfil = request.args.get("perfil")
        userId = request.args.get("userId")

        if not perfil or not userId:
            return jsonify({"error": "Missing perfil or userId"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC spObtenerPermisos @perfil = ?, @userId = ?", (perfil, userId))
        permisos = cursor.fetchall()
        conn.close()

        if permisos:
            return jsonify([{
                "moduloId": p[0],
                "funcionId": p[1],
                "funcion": p[2]
            } for p in permisos]), 200
        else:
            return jsonify({"error": "No permissions found"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_db_connection():
    return pyodbc.connect(conn_str)

