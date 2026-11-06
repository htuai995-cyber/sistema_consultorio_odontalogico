from django.db import models
from gestion.models.especialidad import Especialidad


class Odontologo(models.Model):
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]

    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100, verbose_name='Apellidos')
    numero_colegiatura = models.CharField(max_length=30, unique=True, verbose_name='N° de Colegiatura')
    telefono = models.CharField(max_length=20, verbose_name='Teléfono')
    correo = models.EmailField(verbose_name='Correo electrónico')
    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.PROTECT,
        related_name='odontologos',
        verbose_name='Especialidad'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='Activo',
        verbose_name='Estado'
    )

    class Meta:
        db_table = 'odontologo'
        verbose_name = 'Odontólogo'
        verbose_name_plural = 'Odontólogos'
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f'Dr(a). {self.apellidos}, {self.nombres}'

    @property
    def nombre_completo(self):
        return f'Dr(a). {self.nombres} {self.apellidos}'

