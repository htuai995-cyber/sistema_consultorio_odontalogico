"""
Script para poblar la base de datos con datos de prueba
Ejecución: python manage.py shell < seed_data.py
O bien: python seed_data.py
"""
import os
import sys
import django
from datetime import date, time, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from gestion.models import Especialidad, Paciente, Odontologo, Cita, Diagnostico, Tratamiento, Receta

def poblar():
    print("Creando usuario administrador...")
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@sonrisaperfecta.pe', 'admin123')
        print(" Superusuario creado: admin / admin123")
    else:
        print("  Superusuario admin ya existe.")

    print("Creando especialidades...")
    esp_orto, _ = Especialidad.objects.get_or_create(
        nombre='Ortodoncia',
        defaults={'descripcion': 'Corrección de dientes y mandíbulas posicionadas incorrectamente.', 'estado': 'Activa'}
    )
    esp_endo, _ = Especialidad.objects.get_or_create(
        nombre='Endodoncia',
        defaults={'descripcion': 'Tratamiento del tejido pulpar del diente (conductos).', 'estado': 'Activa'}
    )
    esp_impl, _ = Especialidad.objects.get_or_create(
        nombre='Implantología',
        defaults={'descripcion': 'Colocación y rehabilitación de implantes dentales.', 'estado': 'Activa'}
    )
    esp_pedi, _ = Especialidad.objects.get_or_create(
        nombre='Odontopediatría',
        defaults={'descripcion': 'Atención odontológica integral a niños y adolescentes.', 'estado': 'Activa'}
    )
    esp_rehab, _ = Especialidad.objects.get_or_create(
        nombre='Rehabilitación Oral',
        defaults={'descripcion': 'Recuperación de la estética y función dental integral.', 'estado': 'Activa'}
    )

    print("Creando odontólogos...")
    odo1, _ = Odontologo.objects.get_or_create(
        numero_colegiatura='COP-12345',
        defaults={
            'nombres': 'Carlos Alberto',
            'apellidos': 'Gómez Mendoza',
            'telefono': '987654321',
            'correo': 'carlos.gomez@sonrisaperfecta.pe',
            'especialidad': esp_orto,
            'estado': 'Activo'
        }
    )
    odo2, _ = Odontologo.objects.get_or_create(
        numero_colegiatura='COP-67890',
        defaults={
            'nombres': 'Ana Lucía',
            'apellidos': 'Vásquez Paredes',
            'telefono': '912345678',
            'correo': 'ana.vasquez@sonrisaperfecta.pe',
            'especialidad': esp_endo,
            'estado': 'Activo'
        }
    )
    odo3, _ = Odontologo.objects.get_or_create(
        numero_colegiatura='COP-11223',
        defaults={
            'nombres': 'Roberto',
            'apellidos': 'Morales Castro',
            'telefono': '955443322',
            'correo': 'roberto.morales@sonrisaperfecta.pe',
            'especialidad': esp_impl,
            'estado': 'Activo'
        }
    )

    print("Creando pacientes...")
    pac1, _ = Paciente.objects.get_or_create(
        dni='45678901',
        defaults={
            'nombres': 'María Elena',
            'apellidos': 'Fernández Rojas',
            'fecha_nacimiento': date(1992, 5, 14),
            'telefono': '944332211',
            'direccion': 'Av. Larco 456, Miraflores',
            'correo': 'maria.fernandez@gmail.com'
        }
    )
    pac2, _ = Paciente.objects.get_or_create(
        dni='78901234',
        defaults={
            'nombres': 'Jorge Luis',
            'apellidos': 'Ramírez Torres',
            'fecha_nacimiento': date(1985, 11, 20),
            'telefono': '922114455',
            'direccion': 'Jr. Huancavelica 234, Lima',
            'correo': 'jorge.ramirez@hotmail.com'
        }
    )
    pac3, _ = Paciente.objects.get_or_create(
        dni='12345678',
        defaults={
            'nombres': 'Sofía Alejandra',
            'apellidos': 'Chávez Navarro',
            'fecha_nacimiento': date(2001, 3, 8),
            'telefono': '966778899',
            'direccion': 'Calle Las Flores 789, San Isidro',
            'correo': 'sofia.chavez@gmail.com'
        }
    )

    print("Creando citas...")
    cita1, _ = Cita.objects.get_or_create(
        paciente=pac1,
        fecha=date.today(),
        hora=time(9, 0),
        defaults={
            'odontologo': odo1,
            'motivo': 'Control mensual de brackets',
            'estado': 'Atendida',
            'observaciones': 'Paciente refiere molestias leves en el arco superior.'
        }
    )
    cita2, _ = Cita.objects.get_or_create(
        paciente=pac2,
        fecha=date.today(),
        hora=time(10, 30),
        defaults={
            'odontologo': odo2,
            'motivo': 'Dolor agudo en molar inferior derecho',
            'estado': 'Atendida',
            'observaciones': 'Sensibilidad al frío y al calor.'
        }
    )
    cita3, _ = Cita.objects.get_or_create(
        paciente=pac3,
        fecha=date.today() + timedelta(days=2),
        hora=time(15, 0),
        defaults={
            'odontologo': odo3,
            'motivo': 'Evaluación para implante dental',
            'estado': 'Confirmada',
            'observaciones': 'Traer tomografía panorámica.'
        }
    )

    print("Creando diagnósticos...")
    diag1, _ = Diagnostico.objects.get_or_create(
        cita=cita1,
        defaults={
            'descripcion': 'Maloclusión Clase II. Evolución favorable del tratamiento de ortodoncia fija.',
            'recomendaciones': 'Continuar con el uso de elásticos intermaxilares y cepillado prolijo.',
            'fecha': date.today()
        }
    )
    diag2, _ = Diagnostico.objects.get_or_create(
        cita=cita2,
        defaults={
            'descripcion': 'Pulpitis irreversible en pieza 46 por caries profunda penetrante.',
            'recomendaciones': 'Tratamiento de endodoncia de urgencia. Evitar masticar por el lado derecho.',
            'fecha': date.today()
        }
    )

    print("Creando tratamientos...")
    Tratamiento.objects.get_or_create(
        diagnostico=diag1,
        nombre='Ortodoncia Fija Metálica',
        defaults={
            'descripcion': 'Alineamiento y nivelación dental bimaxilar con brackets de acero inoxidable.',
            'fecha_inicio': date.today() - timedelta(days=90),
            'fecha_fin': date.today() + timedelta(days=270),
            'costo': Decimal('2800.00'),
            'estado': 'En proceso'
        }
    )
    Tratamiento.objects.get_or_create(
        diagnostico=diag2,
        nombre='Endodoncia Molar (Pieza 46)',
        defaults={
            'descripcion': 'Biopulpectomía total, instrumentación rotatoria y obturación tridimensional.',
            'fecha_inicio': date.today(),
            'fecha_fin': date.today() + timedelta(days=7),
            'costo': Decimal('450.00'),
            'estado': 'En proceso'
        }
    )

    print("Creando recetas...")
    Receta.objects.get_or_create(
        diagnostico=diag2,
        medicamento='Amoxicilina 500mg + Ácido Clavulánico 125mg',
        defaults={
            'dosis': '1 tableta',
            'frecuencia': 'Cada 8 horas',
            'duracion': '7 días',
            'indicaciones': 'Tomar con las comidas. No suspender el tratamiento antes de tiempo.',
            'fecha_emision': date.today()
        }
    )
    Receta.objects.get_or_create(
        diagnostico=diag2,
        medicamento='Ibuprofeno 400mg',
        defaults={
            'dosis': '1 tableta',
            'frecuencia': 'Cada 8 horas condicional al dolor',
            'duracion': '3 días',
            'indicaciones': 'Tomar con abundante agua después de los alimentos.',
            'fecha_emision': date.today()
        }
    )

    print("\n Datos de prueba cargados con éxito!")
    print("--------------------------------------------------")
    print(" Credenciales de acceso:")
    print("   Usuario: admin")
    print("   Contraseña: admin123")
    print("--------------------------------------------------")

if __name__ == '__main__':
    poblar()

