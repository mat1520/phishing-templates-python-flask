# 🎯 Phishing Templates - Flask Server

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![Stars](https://img.shields.io/github/stars/mat1520/phishing-templates-python-flask?style=social)

**🚀 Servidor Flask profesional para gestión de templates de phishing educativo**

*Herramienta educativa para pruebas de penetración y concienciación en ciberseguridad*

[📖 Documentación](#-documentación) • [🚀 Instalación](#-instalación-rápida) • [💡 Características](#-características) • [🎥 Demo](#-demo) • [🤝 Contribuir](#-contribuir)

</div>

---

## 🌟 ¿Por qué elegir este proyecto?

- **🎨 Interfaz Moderna**: Panel de administración con diseño dark mode profesional
- **⚡ Despliegue Rápido**: Un clic para activar cualquier template
- **📊 Monitoreo en Tiempo Real**: Visualización instantánea de credenciales capturadas
- **🔒 Base de Datos Segura**: SQLite con thread-safety para múltiples conexiones
- **🌐 Multiplataforma**: Compatible con Windows, Linux y macOS
- **📱 Responsive**: Funciona perfectamente en dispositivos móviles

## 💡 Características

### 🎯 Core Features
- ✅ **30+ Templates Profesionales** - Facebook, Google, Instagram, LinkedIn, etc.
- ✅ **Panel de Control Intuitivo** - Gestión visual de todos los sitios
- ✅ **Captura Automática** - Credenciales, IPs y User-Agents
- ✅ **API REST** - Acceso programático a los datos
- ✅ **Hot-Deploy** - Activar/desactivar sitios sin reiniciar
- ✅ **Logs Detallados** - Tracking completo de actividad

### 🛡️ Seguridad y Performance
- ✅ **Thread-Safe** - Manejo seguro de múltiples conexiones
- ✅ **Error Handling** - Gestión robusta de errores
- ✅ **Static Files** - Servido optimizado de recursos
- ✅ **MIME Types** - Detección automática de tipos de archivo

## 🚀 Instalación Rápida

### Prerrequisitos
```bash
Python 3.7+
Flask 2.0+
```

### 1️⃣ Clona el repositorio
```bash
git clone https://github.com/mat1520/phishing-templates-python-flask.git
cd phishing-templates-python-flask
```

### 2️⃣ Instala dependencias
```bash
pip install flask
```

### 3️⃣ Ejecuta el servidor
```bash
python app.py
```

### 4️⃣ ¡Disfruta! 🎉
```
🌐 Servidor: http://localhost:5000
👨‍💼 Admin Panel: http://localhost:5000/admin
```

## 📖 Documentación

### 🎮 Uso Básico

1. **Selecciona un Template**
   - Ve a `http://localhost:5000`
   - Elige uno de los 30+ templates disponibles
   - Haz clic en "Deploy" para activarlo

2. **Captura Credenciales**
   - Comparte la URL del phishing: `http://localhost:5000/phish/[sitio]/`
   - Las credenciales se guardan automáticamente

3. **Monitorea Resultados**
   - Ve al panel de admin: `http://localhost:5000/admin`
   - Visualiza todas las credenciales capturadas en tiempo real

### 📁 Estructura del Proyecto

```
phishing-templates-python-flask/
├── 📱 app.py                    # Servidor Flask principal
├── 🗃️ credentials.db            # Base de datos SQLite
├── 🖼️ logos/                    # Logos de las marcas
│   ├── facebook.jpg
│   ├── google.jpg
│   └── ...
├── 🌐 sites/                    # Templates de phishing
│   ├── facebook/
│   ├── google/
│   ├── instagram/
│   └── ...
└── 🎨 templates/                # Templates HTML del panel
    ├── index_dark.html
    ├── admin_dark.html
    └── site_status_dark.html
```

### 🔧 API Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Panel principal |
| `/admin` | GET | Panel de administración |
| `/deploy/<site>` | GET | Desplegar sitio |
| `/stop/<site>` | GET | Detener sitio |
| `/phish/<site>/` | GET | Acceder al template |
| `/api/credentials` | GET | API REST credenciales |

## 🎥 Demo

### 📸 Screenshots

<details>
<summary>🖼️ Ver capturas de pantalla</summary>

**Panel Principal**
```
🎯 Phishing Templates - Panel de Control
┌─────────────────────────────────────────┐
│ [🟢 Deploy] Facebook     📊 Capturas: 12│
│ [🔴 Stop  ] Google       📊 Capturas: 8 │
│ [🟢 Deploy] Instagram    📊 Capturas: 5 │
│ [🟢 Deploy] LinkedIn     📊 Capturas: 3 │
└─────────────────────────────────────────┘
```

**Panel de Administración**
```
👨‍💼 Credenciales Capturadas
┌─────────────────────────────────────────┐
│ 📧 Email         🔐 Password    📍 IP   │
│ user@gmail.com   123456         1.1.1.1 │
│ admin@test.com   password       2.2.2.2 │
└─────────────────────────────────────────┘
```

</details>

### 🎬 Video Tutorial

[![Video Tutorial](https://img.shields.io/badge/▶️%20Video%20Tutorial-YouTube-red)](https://youtube.com)

## 🛡️ Uso Ético y Legal

> **⚠️ IMPORTANTE**: Esta herramienta está diseñada EXCLUSIVAMENTE para:
> 
> - 🎓 **Educación en Ciberseguridad**
> - 🔍 **Pruebas de Penetración Autorizadas**
> - 🧪 **Entornos de Laboratorio Controlados**
> - 📚 **Investigación Académica**

### 📋 Responsabilidades del Usuario

- ✅ Obtener autorización explícita antes de usar
- ✅ Usar solo en entornos controlados
- ✅ Respetar las leyes locales e internacionales
- ✅ No usar para actividades maliciosas

**El autor NO se hace responsable del uso indebido de esta herramienta.**

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! 🎉

### 🔥 Formas de Contribuir

1. **🐛 Reporta Bugs**
   - Abre un [issue](https://github.com/mat1520/phishing-templates-python-flask/issues)
   - Describe el problema detalladamente

2. **💡 Sugiere Features**
   - Propón nuevas características
   - Mejoras en la interfaz

3. **🎨 Añade Templates**
   - Crea nuevos templates de sitios
   - Mejora los existentes

4. **📝 Mejora Documentación**
   - Traducciones
   - Ejemplos adicionales

### 🚀 Proceso de Contribución

```bash
# 1. Fork el proyecto
git fork https://github.com/mat1520/phishing-templates-python-flask

# 2. Crea una rama
git checkout -b feature/nueva-caracteristica

# 3. Haz commits
git commit -am 'Añade nueva característica'

# 4. Push a la rama
git push origin feature/nueva-caracteristica

# 5. Abre un Pull Request
```

##  Soporte y Contacto

### 💬 Obtén Ayuda

- 📧 **Email**: [contacto@mat1520.dev](mailto:contacto@mat1520.dev)
- 💬 **Telegram**: [@MAT3810](https://t.me/MAT3810)
- 🐛 **Issues**: [GitHub Issues](https://github.com/mat1520/phishing-templates-python-flask/issues)
- 💭 **Discussions**: [GitHub Discussions](https://github.com/mat1520/phishing-templates-python-flask/discussions)

### 🌐 Sígueme

- 🐙 **GitHub**: [@mat1520](https://github.com/mat1520)
- 🐦 **Twitter**: [@mat1520dev](https://twitter.com/mat1520dev)
- 💼 **LinkedIn**: [MAT1520](https://linkedin.com/in/mat1520)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2025 MAT1520

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**⭐ Si este proyecto te ayudó, no olvides darle una estrella ⭐**

**🔥 ¡Hecho con ❤️ por [MAT1520](https://github.com/mat1520)! 🔥**

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=mat1520.phishing-templates-python-flask)

</div>
