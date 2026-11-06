from django.db import models


class Paciente(models.Model):
    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100, verbose_name='Apellidos')
    dni = models.CharField(max_length=8, unique=True, verbose_name='DNI')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    telefono = models.CharField(max_length=20, verbose_name='Teléfono')
    direccion = models.CharField(max_length=200, verbose_name='Dirección')
    correo = models.EmailField(verbose_name='Correo electrónico')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    class Meta:
        db_table = 'paciente'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f'{self.apellidos}, {self.nombres}'

    @property
    def nombre_completo(self):
        return f'{self.nombres} {self.apellidos}'

