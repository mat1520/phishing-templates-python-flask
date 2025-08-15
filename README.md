# 🎯 Servidor Flask de Phishing

Un servidor Flask profesional para despliegue y gestión de sitios de phishing con captura de credenciales.

## ⚠️ ADVERTENCIA LEGAL

**SOLO PARA FINES EDUCATIVOS Y PRUEBAS DE SEGURIDAD AUTORIZADAS**

Este software está diseñado exclusivamente para:
- Educación en ciberseguridad
- Pruebas de penetración autorizadas
- Evaluaciones de seguridad internas
- Investigación académica

El uso no autorizado de esta herramienta puede ser ilegal. El usuario es completamente responsable del uso apropiado y legal de este software.

## 🚀 Características

- **Interfaz Web Moderna**: Panel de control intuitivo con diseño responsive
- **Múltiples Sitios**: Soporte para 30+ plantillas de phishing preconfiguradas
- **Base de Datos**: Sistema de almacenamiento SQLite con thread safety
- **Captura Completa**: Registra credenciales, IPs, user agents y datos adicionales
- **Panel de Administración**: Visualización en tiempo real de datos capturados
- **Exportación**: Descarga de datos en formato JSON
- **Filtrado**: Búsqueda y filtrado por sitios específicos
- **Seguridad**: Procesamiento seguro de formularios y datos

## 📋 Requisitos Previos

- Python 3.7 o superior
- Pip (gestor de paquetes de Python)
- Navegador web moderno

## 🛠️ Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   git clone [repositorio]
   cd phishing-templates-python-flask
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verificar estructura de carpetas**
   ```
   phishing-templates-python-flask/
   ├── app.py
   ├── requirements.txt
   ├── templates/
   │   ├── index.html
   │   └── admin.html
   └── sites/
       ├── facebook/
       ├── google/
       ├── instagram/
       └── ... (otros sitios)
   ```

## 🚀 Uso

### Iniciar el Servidor

```bash
python app.py
```

El servidor se iniciará en `http://localhost:5000`

### Acceso a las Interfaces

- **Panel Principal**: `http://localhost:5000`
  - Selección y despliegue de sitios
  - Vista general de sitios disponibles

- **Panel de Administración**: `http://localhost:5000/admin`
  - Visualización de credenciales capturadas
  - Estadísticas en tiempo real
  - Exportación de datos

### Desplegar un Sitio

1. Accede al panel principal (`http://localhost:5000`)
2. Selecciona el sitio que deseas desplegar
3. Haz clic en "🚀 Desplegar" 
4. El sitio estará disponible en `http://localhost:5000/site/[nombre-sitio]/`

### Monitorear Capturas

1. Accede al panel de administración (`http://localhost:5000/admin`)
2. Las credenciales aparecerán en tiempo real
3. Usa los filtros para buscar por sitio específico
4. Exporta los datos usando el botón "💾 Exportar JSON"

## 📁 Estructura de Sitios

Cada sitio en la carpeta `sites/` debe contener:

```
sites/[nombre-sitio]/
├── index.php         # Página principal (opcional)
├── login.html        # Formulario de login
├── login.php         # Procesador (será manejado por Flask)
├── mobile.html       # Versión móvil (opcional)
└── [archivos estáticos] # CSS, JS, imágenes, etc.
```

## 🔧 Configuración Avanzada

### Cambiar Puerto

Edita `app.py` y modifica la línea final:

```python
app.run(debug=True, host='0.0.0.0', port=PUERTO_DESEADO)
```

### Acceso Remoto

Para permitir acceso desde otras máquinas en la red:

```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

### Base de Datos

- Los datos se almacenan en `credentials.db` (SQLite)
- Se crean automáticamente las tablas necesarias
- Thread-safe para múltiples conexiones simultáneas

## 📊 Datos Capturados

El sistema registra:

- **Credenciales**: Email/usuario y contraseña
- **Información del Cliente**: IP, User-Agent
- **Metadatos**: Timestamp, sitio utilizado
- **Datos Adicionales**: Todos los campos del formulario en JSON

## 🛡️ Características de Seguridad

- Procesamiento seguro de formularios
- Validación de entrada
- Thread-safe database operations
- Filtrado XSS básico en templates
- Manejo seguro de errores

## 🔍 Sitios Incluidos

- Facebook (múltiples variantes)
- Google/Gmail
- Instagram
- GitHub
- LinkedIn
- Twitter
- Netflix
- Spotify
- PayPal
- Microsoft
- Y muchos más...

## 🚨 Consideraciones de Seguridad

1. **Firewall**: Asegúrate de que el puerto esté protegido
2. **Acceso**: Limita el acceso solo a IPs autorizadas
3. **Logs**: Revisa regularmente los logs del sistema
4. **Datos**: Elimina datos sensibles después de las pruebas

## 🐛 Solución de Problemas

### Error de Puerto en Uso
```bash
# Cambiar puerto en app.py o matar proceso
netstat -ano | findstr :5000
taskkill /PID [PID] /F
```

### Error de Permisos de Base de Datos
```bash
# Verificar permisos del directorio
chmod 755 .
chmod 644 credentials.db
```

### Sitios No Cargan
- Verificar que la carpeta `sites/` existe
- Comprobar que los archivos HTML/PHP están presentes
- Revisar logs de consola para errores

## 📝 Registro de Cambios

### v1.0.0
- Servidor Flask completo
- Panel de administración web
- Base de datos SQLite
- Soporte para múltiples sitios
- Exportación de datos

## 🤝 Contribuciones

Para contribuir:

1. Fork del repositorio
2. Crear rama para nueva característica
3. Commit de cambios
4. Push a la rama
5. Crear Pull Request

## 📄 Licencia

Este proyecto es solo para fines educativos. Consulta las leyes locales antes de usar.

## ⭐ Reconocimientos

- Plantillas de phishing de la comunidad
- Framework Flask
- Diseño UI moderno con CSS3

---

**Recuerda**: Usa esta herramienta de manera responsable y ética. El conocimiento de seguridad debe usarse para proteger, no para dañar.
