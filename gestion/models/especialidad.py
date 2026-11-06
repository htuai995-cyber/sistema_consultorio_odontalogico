from django.db import models


class Especialidad(models.Model):
    ESTADO_CHOICES = [
        ('Activa', 'Activa'),
        ('Inactiva', 'Inactiva'),
    ]

    nombre = models.CharField(max_length=100, verbose_name='Nombre de especialidad')
    descripcion = models.TextField(verbose_name='Descripción')
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='Activa',
        verbose_name='Estado'
    )

    class Meta:
        db_table = 'especialidad'
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

