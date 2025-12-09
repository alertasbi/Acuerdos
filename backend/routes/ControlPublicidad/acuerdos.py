import os
import pyodbc
from flask import Flask, Blueprint, request, jsonify
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()
acuerdos_bp = Blueprint('acuerdos', __name__)
acuerdosHoteles_bp = Blueprint('acuerdosHoteles', __name__)
editarAcuerdo_bp = Blueprint('editarAcuerdo', __name__)
eliminarAcuerdo_bp = Blueprint('eliminarAcuerdo', __name__)

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
@acuerdos_bp.get('/acuerdos')
def get_acuerdos():
    try:
        userId = request.args.get("userId")

        if not userId:
            return jsonify({"error": "Missing userId"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC spConsultaVistaControlPublicidadTest @usuario = ?", (userId,))
        acuerdo = cursor.fetchall()
        conn.close()

        return jsonify([{
            #"message": "Consulta exitosa",
            "Fila": row[0],
			"Registro": row[1],
			"Equipo": row[2],
			"Año": row[3],
			"Mes": row[4],
			"TipoAcuerdo": row[5],
			"Gerente": row[6],
			"Proveedor": row[7],
			"ID": row[8],
			"MonedaAcuerdo": row[9],
			"PrecioSinIVA": row[10],
			"FolioAcuerdo": row[11],
			"MesesContratados": row[12],
			"FechaInicioAccionesEfectivasMKT": row[13],
			"FechaFinAccionesEfectivasMKT": row[14],
			"MesesAccionesEfectivasMKT": row[15],
			"FechaVenta": row[16],
			"RFC": row[17],
			"FormaPago": row[18],
			"ComentariosAdicionales": row[19],
			"Firmado": row[20],
			"ControlAcuerdos": row[21],
			"ArchivoSinMontos": row[22],
			"FolioFactura": row[23],
			"ComentariosFinanzas": row[24],
			"CantidadFacturas": row[25],
			"CantidadFacturados": row[26],
			"MonedaFactura": row[27],
			"ImporteFacturarConIVA": row[28],
			"MontoFacturado": row[29],
			"MontoFacturadoPesosMXSinIVA": row[30],
			"MontoCobrado": row[31],
			"FechaCobro": row[32],
			"DiferenciaPorCobrarContraFacturado": row[33],
			"EstatusCXC": row[34],
			"Provider": row[35],
			"IDs": row[36],
			"FolioFacturaExtendido": row[37]
        } for row in acuerdo]), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@acuerdosHoteles_bp.get('/acuerdosHoteles')
def get_acuerdosHoteles():
    try:
        controlPublicidadId = request.args.get("controlPublicidadId")
        opcion = request.args.get("opcion")
        userId = request.args.get("userId")

        if not userId or not controlPublicidadId or not opcion:
            return jsonify({"error": "Missing userId, controlPublicidadId or opcion"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC spfctControlPublicidadConsulta @idControlPublicidad = ?, @opcion = ?, @usuario = ?", (controlPublicidadId, opcion, userId))
        acuerdoDetalle = cursor.fetchall()
        conn.close()

        return jsonify([{
            #"message": "Consulta exitosa",
            "idCP": row[0],
			"ID": row[1],
			"Nombre": row[2],
			"TipoServicio": row[3]
        } for row in acuerdoDetalle]), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_db_connection():
    return pyodbc.connect(conn_str)
