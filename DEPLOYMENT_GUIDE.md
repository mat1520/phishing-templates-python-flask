# Configuración del Servidor de Phishing Flask
# =============================================

## 🚀 NUEVO SISTEMA DE DESPLIEGUE

El servidor ahora incluye las siguientes mejoras:

### ✨ Características Principales

1. **Despliegue por Puertos Independientes**
   - Cada sitio se despliega en su propio puerto (5001, 5002, 5003, etc.)
   - Los sitios funcionan como servidores completamente independientes
   - Más realista para las víctimas (parece un sitio real)

2. **Logos Automáticos**
   - Se cargan automáticamente desde la carpeta `logos/`
   - Mapeo inteligente de nombres de sitios a logos
   - Interfaz visual más profesional

3. **Estado en Tiempo Real**
   - Panel de control que muestra qué sitios están activos
   - Información de puertos y URLs de acceso
   - Capacidad de detener sitios individualmente

### 📋 Cómo Usar el Sistema Mejorado

1. **Acceder al Panel Principal:**
   ```
   http://localhost:5000
   ```

2. **Desplegar un Sitio:**
   - Selecciona un sitio del panel
   - Haz clic en "🚀 Desplegar"
   - El sistema automáticamente:
     * Encuentra un puerto libre
     * Crea un servidor Flask independiente
     * Te muestra la información de acceso

3. **Acceder al Sitio Desplegado:**
   ```
   http://localhost:PUERTO_ASIGNADO
   ```
   Ejemplo: `http://localhost:5001` para Facebook

4. **Monitorear Capturas:**
   ```
   http://localhost:5000/admin
   ```

### 🌐 Ventajas del Nuevo Sistema

- **Más Realista:** Cada sitio tiene su propia URL y puerto
- **Mejor Performance:** Sitios independientes no interfieren entre sí
- **Fácil Compartir:** Puedes dar diferentes URLs a diferentes personas
- **Red Local:** Accesible desde otros dispositivos en la misma red
- **Gestión Simple:** Detener/iniciar sitios individualmente

### 📱 Acceso desde Red Local

Para acceder desde otros dispositivos en tu red:

1. **Encuentra tu IP local:**
   ```cmd
   ipconfig
   ```

2. **Usa la IP en lugar de localhost:**
   ```
   http://TU_IP_LOCAL:PUERTO
   ```
   Ejemplo: `http://192.168.1.100:5001`

### 🔧 Configuración de Puertos

- **Puerto Principal:** 5000 (Panel de control)
- **Puertos de Sitios:** 5001-5999 (Asignación automática)
- **Base de Datos:** SQLite local (credentials.db)

### ⚡ Comandos Rápidos

```bash
# Iniciar servidor
python app.py

# Ver sitios desplegados
curl http://localhost:5000/deployed-sites

# Detener todos los sitios
Ctrl+C en la terminal principal
```

### 🛡️ Configuración de Firewall

Para permitir acceso externo:

```cmd
# Windows Firewall
netsh advfirewall firewall add rule name="Flask Phishing" dir=in action=allow protocol=TCP localport=5000-5999

# O usar Windows Defender con interfaz gráfica
```

### 📊 Monitoreo

El sistema registra:
- Credenciales capturadas
- IPs de acceso
- User agents
- Timestamps
- Datos adicionales del formulario

### 🔄 Actualizaciones Futuras

- [ ] Certificados SSL automáticos
- [ ] Dominios personalizados con DNS local
- [ ] Webhooks para notificaciones
- [ ] Plantillas de email de phishing
- [ ] Análisis de comportamiento de víctimas

---

**¡El servidor ahora es mucho más potente y realista!** 🎯
