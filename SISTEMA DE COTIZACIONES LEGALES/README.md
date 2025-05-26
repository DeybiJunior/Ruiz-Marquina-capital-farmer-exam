# 📋 Sistema de Cotizaciones Legales

Sistema web profesional para la gestión y generación de cotizaciones de servicios jurídicos, desarrollado con Flask y SQLite.

## 🚀 Características Principales

- **Generación Automática de Cotizaciones**: Sistema que crea números únicos de cotización con formato COT-AAAA-####
- **Base de Datos SQLite**: Almacenamiento persistente de todas las cotizaciones
- **Panel de Administración**: Vista completa de cotizaciones con estadísticas
- **Interfaz Responsive**: Diseño moderno que se adapta a dispositivos móviles
- **Validación de Datos**: Verificación de campos obligatorios y tipos de servicio
- **Precios Predefinidos**: Tarifas establecidas para diferentes servicios legales

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3.x, Flask, SQLite3
- **Frontend**: HTML5, CSS3, JavaScript ES6
- **Base de Datos**: SQLite
- **Librerías**: Flask-CORS para manejo de CORS

## 📁 Estructura del Proyecto

```
sistema-cotizaciones-legales/
├── README.md
├── app.py                  # Aplicación principal Flask
├── requirements.txt        # Dependencias Python
├── database.db            # Base de datos SQLite (se genera automáticamente)
├── templates/
│   ├── index.html         # Formulario de cotización
│   └── admin.html         # Panel de administración
└── static/
    ├── styles.css         # Estilos CSS
    └── script.js          # JavaScript frontend
```

## 🔧 Instalación y Configuración

### Prerrequisitos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/apellido-capital-farmer-exam.git
   cd apellido-capital-farmer-exam
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

4. **Acceder a la aplicación**
   - Formulario de cotización: http://localhost:5000
   - Panel de administración: http://localhost:5000/admin

## 🖥️ Uso del Sistema

### Generar Cotización
1. Accede a la página principal (http://localhost:5000)
2. Completa el formulario con:
   - Nombre completo del cliente
   - Correo electrónico
   - Tipo de servicio requerido
   - Descripción del caso (opcional)
3. Haz clic en "Generar Cotización"
4. El sistema mostrará el número de cotización y precio

### Panel de Administración
1. Accede a http://localhost:5000/admin
2. Visualiza todas las cotizaciones generadas
3. Consulta estadísticas generales:
   - Total de cotizaciones
   - Ingresos potenciales
   - Servicio más solicitado

## 🔗 API Endpoints

### POST /generar_cotizacion
Genera una nueva cotización

**Body (JSON):**
```json
{
  "nombre": "Juan Pérez",
  "email": "juan@email.com",
  "tipo_servicio": "constitucion",
  "descripcion": "Constitución de empresa SAC"
}
```

**Respuesta exitosa:**
```json
{
  "numero_cotizacion": "COT-2025-0001",
  "nombre_cliente": "Juan Pérez",
  "email": "juan@email.com",
  "tipo_servicio": "Constitución de Empresa",
  "precio": 1500,
  "fecha_creacion": "2025-05-26T10:30:00"
}
```

### GET /cotizaciones
Obtiene todas las cotizaciones registradas

**Respuesta:**
```json
[
  {
    "numero_cotizacion": "COT-2025-0001",
    "nombre_cliente": "Juan Pérez",
    "email": "juan@email.com",
    "tipo_servicio": "Constitución de Empresa",
    "precio": 1500,
    "fecha_creacion": "2025-05-26T10:30:00"
  }
]
```

## 🗄️ Base de Datos

### Esquema de la tabla `cotizaciones`

```sql
CREATE TABLE cotizaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_cotizacion TEXT UNIQUE NOT NULL,
    nombre_cliente TEXT NOT NULL,
    email TEXT NOT NULL,
    tipo_servicio TEXT NOT NULL,
    descripcion_caso TEXT,
    precio REAL NOT NULL,
    fecha_creacion DATETIME NOT NULL
);
```

## 🔒 Validaciones

- **Campos obligatorios**: nombre, email, tipo_servicio
- **Formato de email**: Validación HTML5 y backend
- **Tipos de servicio válidos**: constitucion, defensa_laboral, consultoria_tributaria
- **Números de cotización únicos**: Generación automática sin duplicados

## 🎨 Características de Diseño

- **Diseño responsive**: Compatible con dispositivos móviles
- **Gradientes modernos**: Interfaz visual atractiva
- **Animaciones suaves**: Efectos hover y transiciones
- **Estados de carga**: Indicadores visuales durante procesos
- **Manejo de errores**: Mensajes informativos para el usuario

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@DeybiJunior](https://github.com/DeybiJunior)
- Email: deybijuniorr@gmail.com

⭐ Si este proyecto te resulta útil, ¡no olvides darle una estrella en GitHub!