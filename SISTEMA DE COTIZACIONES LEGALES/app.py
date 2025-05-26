from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Configuración de precios
PRECIOS = {
    'constitucion': 1500,
    'defensa_laboral': 2000,
    'consultoria_tributaria': 800
}

def init_db():
    """Inicializa la base de datos SQLite"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cotizaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_cotizacion TEXT UNIQUE NOT NULL,
            nombre_cliente TEXT NOT NULL,
            email TEXT NOT NULL,
            tipo_servicio TEXT NOT NULL,
            descripcion_caso TEXT,
            precio REAL NOT NULL,
            fecha_creacion DATETIME NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def generar_numero_cotizacion():
    """Genera un número de cotización único"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Obtener el último número de cotización del año actual
    año_actual = datetime.now().year
    cursor.execute('''
        SELECT numero_cotizacion FROM cotizaciones 
        WHERE numero_cotizacion LIKE ? 
        ORDER BY id DESC LIMIT 1
    ''', (f'COT-{año_actual}-%',))
    
    resultado = cursor.fetchone()
    
    if resultado:
        ultimo_numero = int(resultado[0].split('-')[2])
        nuevo_numero = ultimo_numero + 1
    else:
        nuevo_numero = 1
    
    conn.close()
    return f"COT-{año_actual}-{nuevo_numero:04d}"

@app.route('/')
def index():
    """Página principal con el formulario"""
    return render_template('index.html')

@app.route('/generar_cotizacion', methods=['POST'])
def generar_cotizacion():
    """Endpoint para generar una nueva cotización"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['nombre', 'email', 'tipo_servicio']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'El campo {field} es requerido'}), 400
        
        # Validar tipo de servicio
        if data['tipo_servicio'] not in PRECIOS:
            return jsonify({'error': 'Tipo de servicio no válido'}), 400
        
        # Generar datos de la cotización
        numero_cotizacion = generar_numero_cotizacion()
        precio = PRECIOS[data['tipo_servicio']]
        fecha_creacion = datetime.now()
        
        # Guardar en base de datos
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO cotizaciones 
            (numero_cotizacion, nombre_cliente, email, tipo_servicio, descripcion_caso, precio, fecha_creacion)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            numero_cotizacion,
            data['nombre'],
            data['email'],
            data['tipo_servicio'],
            data.get('descripcion', ''),
            precio,
            fecha_creacion
        ))
        
        conn.commit()
        conn.close()
        
        # Mapear nombres de servicios para respuesta
        nombres_servicios = {
            'constitucion': 'Constitución de Empresa',
            'defensa_laboral': 'Defensa Laboral',
            'consultoria_tributaria': 'Consultoría Tributaria'
        }
        
        # Respuesta exitosa
        response = {
            'numero_cotizacion': numero_cotizacion,
            'nombre_cliente': data['nombre'],
            'email': data['email'],
            'tipo_servicio': nombres_servicios[data['tipo_servicio']],
            'descripcion_caso': data.get('descripcion', ''),
            'precio': precio,
            'fecha_creacion': fecha_creacion.isoformat()
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cotizaciones', methods=['GET'])
def listar_cotizaciones():
    """Endpoint para listar todas las cotizaciones"""
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT numero_cotizacion, nombre_cliente, email, tipo_servicio, precio, fecha_creacion
            FROM cotizaciones
            ORDER BY fecha_creacion DESC
        ''')
        
        cotizaciones = []
        nombres_servicios = {
            'constitucion': 'Constitución de Empresa',
            'defensa_laboral': 'Defensa Laboral',
            'consultoria_tributaria': 'Consultoría Tributaria'
        }
        
        for row in cursor.fetchall():
            cotizaciones.append({
                'numero_cotizacion': row[0],
                'nombre_cliente': row[1],
                'email': row[2],
                'tipo_servicio': nombres_servicios.get(row[3], row[3]),
                'precio': row[4],
                'fecha_creacion': row[5]
            })
        
        conn.close()
        return jsonify(cotizaciones), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin')
def admin_panel():
    """Panel de administración para ver cotizaciones"""
    return render_template('admin.html')

if __name__ == '__main__':
    # Crear directorio templates si no existe
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # Inicializar base de datos al arrancar
    init_db()
    print("🚀 Sistema de Cotizaciones Legales iniciado")
    print("📊 Base de datos SQLite configurada")
    print("🌐 Accede a: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)