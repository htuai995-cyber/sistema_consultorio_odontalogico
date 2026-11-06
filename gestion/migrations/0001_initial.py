# Generated manually for Sonrisa Perfecta
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre de especialidad')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('estado', models.CharField(choices=[('Activa', 'Activa'), ('Inactiva', 'Inactiva')], default='Activa', max_length=20, verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Especialidad',
                'verbose_name_plural': 'Especialidades',
                'db_table': 'especialidad',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100, verbose_name='Nombres')),
                ('apellidos', models.CharField(max_length=100, verbose_name='Apellidos')),
                ('dni', models.CharField(max_length=8, unique=True, verbose_name='DNI')),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha de nacimiento')),
                ('telefono', models.CharField(max_length=20, verbose_name='Teléfono')),
                ('direccion', models.CharField(max_length=200, verbose_name='Dirección')),
                ('correo', models.EmailField(max_length=254, verbose_name='Correo electrónico')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')),
            ],
            options={
                'verbose_name': 'Paciente',
                'verbose_name_plural': 'Pacientes',
                'db_table': 'paciente',
                'ordering': ['apellidos', 'nombres'],
            },
        ),
        migrations.CreateModel(
            name='Odontologo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100, verbose_name='Nombres')),
                ('apellidos', models.CharField(max_length=100, verbose_name='Apellidos')),
                ('numero_colegiatura', models.CharField(max_length=30, unique=True, verbose_name='N° de Colegiatura')),
                ('telefono', models.CharField(max_length=20, verbose_name='Teléfono')),
                ('correo', models.EmailField(max_length=254, verbose_name='Correo electrónico')),
                ('estado', models.CharField(choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')], default='Activo', max_length=20, verbose_name='Estado')),
                ('especialidad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='odontologos', to='gestion.especialidad', verbose_name='Especialidad')),
            ],
            options={
                'verbose_name': 'Odontólogo',
                'verbose_name_plural': 'Odontólogos',
                'db_table': 'odontologo',
                'ordering': ['apellidos', 'nombres'],
            },
        ),
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(verbose_name='Fecha de atención')),
                ('hora', models.TimeField(verbose_name='Hora de atención')),
                ('motivo', models.CharField(max_length=200, verbose_name='Motivo de consulta')),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Confirmada', 'Confirmada'), ('Atendida', 'Atendida'), ('Cancelada', 'Cancelada')], default='Pendiente', max_length=20, verbose_name='Estado')),
                ('observaciones', models.TextField(blank=True, verbose_name='Observaciones')),
                ('odontologo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='citas', to='gestion.odontologo', verbose_name='Odontólogo')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='citas', to='gestion.paciente', verbose_name='Paciente')),
            ],
            options={
                'verbose_name': 'Cita',
                'verbose_name_plural': 'Citas',
                'db_table': 'cita',
                'ordering': ['-fecha', '-hora'],
            },
        ),
        migrations.CreateModel(
            name='Diagnostico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(verbose_name='Diagnóstico clínico')),
                ('recomendaciones', models.TextField(verbose_name='Recomendaciones')),
                ('fecha', models.DateField(verbose_name='Fecha del diagnóstico')),
                ('cita', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='diagnosticos', to='gestion.cita', verbose_name='Cita')),
            ],
            options={
                'verbose_name': 'Diagnóstico',
                'verbose_name_plural': 'Diagnósticos',
                'db_table': 'diagnostico',
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='Tratamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150, verbose_name='Nombre del tratamiento')),
                ('descripcion', models.TextField(verbose_name='Descripción del procedimiento')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de inicio')),
                ('fecha_fin', models.DateField(verbose_name='Fecha de finalización')),
                ('costo', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Costo (S/.)')),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('En proceso', 'En proceso'), ('Finalizado', 'Finalizado')], default='Pendiente', max_length=20, verbose_name='Estado')),
                ('diagnostico', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tratamientos', to='gestion.diagnostico', verbose_name='Diagnóstico')),
            ],
            options={
                'verbose_name': 'Tratamiento',
                'verbose_name_plural': 'Tratamientos',
                'db_table': 'tratamiento',
                'ordering': ['-fecha_inicio'],
            },
        ),
        migrations.CreateModel(
            name='Receta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicamento', models.CharField(max_length=150, verbose_name='Medicamento')),
                ('dosis', models.CharField(max_length=100, verbose_name='Dosis')),
                ('frecuencia', models.CharField(max_length=100, verbose_name='Frecuencia')),
                ('duracion', models.CharField(max_length=100, verbose_name='Duración')),
                ('indicaciones', models.TextField(verbose_name='Indicaciones adicionales')),
                ('fecha_emision', models.DateField(verbose_name='Fecha de emisión')),
                ('diagnostico', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recetas', to='gestion.diagnostico', verbose_name='Diagnóstico')),
            ],
            options={
                'verbose_name': 'Receta',
                'verbose_name_plural': 'Recetas',
                'db_table': 'receta',
                'ordering': ['-fecha_emision'],
            },
        ),
    ]
