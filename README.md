# Sonrisa Perfecta - Consultorio Odontológico 🦷

Sistema de Gestión para Consultorio Odontológico "Sonrisa Perfecta" desarrollado con **Python + Django + MariaDB**.

## Requisitos

- Python 3.10+
- XAMPP (MariaDB corriendo en puerto 3306)
- Entorno virtual `.venv` (ya incluido en el proyecto)

## Instalación y Configuración

### 1. Crear la base de datos

Abrir phpMyAdmin o ejecutar en consola MySQL/MariaDB:

```sql
CREATE DATABASE consultorio_odontologico CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

O ejecutar el script:
```bash
mysql -u root -p < db_setup.sql
```

### 2. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env
# Editar .env con tus credenciales de base de datos
```

### 3. Activar el entorno virtual

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

### 4. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Cargar datos de prueba (Opcional pero recomendado)

```bash
python seed_data.py
```
> Esto creará automáticamente el superusuario `admin` (clave: `admin123`) y registros de ejemplo para pacientes, odontólogos, especialidades, citas, diagnósticos, tratamientos y recetas.

### 6. Ejecutar pruebas automatizadas

```bash
python manage.py test gestion
```

### 7. Ejecutar el servidor

```bash
python manage.py runserver
```

Visitar: http://127.0.0.1:8000

## Módulos del Sistema

| Módulo | URL | Descripción |
|--------|-----|-------------|
| Dashboard | `/` | Indicadores y estadísticas |
| Pacientes | `/pacientes/` | CRUD completo de pacientes |
| Odontólogos | `/odontologos/` | CRUD de odontólogos |
| Especialidades | `/especialidades/` | Gestión de especialidades |
| Citas | `/citas/` | Programación de citas + PDF |
| Diagnósticos | `/diagnosticos/` | Registro clínico + PDF |
| Tratamientos | `/tratamientos/` | Control de tratamientos + PDF |
| Recetas | `/recetas/` | Prescripciones médicas + PDF |

## Modelos (Tablas de Base de Datos)

1. **Especialidad** - Especialidades odontológicas
2. **Paciente** - Datos de pacientes
3. **Odontologo** - Datos del personal médico
4. **Cita** - Programación de atenciones
5. **Diagnostico** - Diagnósticos clínicos
6. **Tratamiento** - Procedimientos dentales
7. **Receta** - Prescripciones médicas

## Tecnologías

- **Backend:** Python 3.x, Django 6.x
- **Base de datos:** MariaDB (via XAMPP)
- **Frontend:** HTML5, CSS3 personalizado, JavaScript, Font Awesome
- **PDF:** ReportLab
- **Autenticación:** Django Auth integrado

## Estructura del Proyecto

```
consultorio_odontologico/
├── .env                      # Variables de entorno (no subir a git)
├── .env.example              # Plantilla de configuración
├── .venv/                    # Entorno virtual Python
├── core/                     # Configuración principal Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── gestion/                  # Aplicación principal
│   ├── models/               # Un modelo por archivo
│   │   ├── especialidad.py
│   │   ├── paciente.py
│   │   ├── odontologo.py
│   │   ├── cita.py
│   │   ├── diagnostico.py
│   │   ├── tratamiento.py
│   │   └── receta.py
│   ├── forms/                # Formularios validados
│   ├── views/                # Vistas por módulo
│   └── urls.py
├── templates/                # Templates HTML
│   ├── base.html
│   ├── registration/
│   └── gestion/
├── static/                   # CSS, JS, imágenes
│   ├── css/style.css
│   └── js/main.js
├── manage.py
└── requirements.txt
```

