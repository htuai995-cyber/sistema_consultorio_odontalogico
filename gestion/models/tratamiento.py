from django.db import models
from gestion.models.diagnostico import Diagnostico


class Tratamiento(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En proceso', 'En proceso'),
        ('Finalizado', 'Finalizado'),
    ]

    diagnostico = models.ForeignKey(
        Diagnostico,
        on_delete=models.PROTECT,
        related_name='tratamientos',
        verbose_name='Diagnóstico'
    )
    nombre = models.CharField(max_length=150, verbose_name='Nombre del tratamiento')
    descripcion = models.TextField(verbose_name='Descripción del procedimiento')
    fecha_inicio = models.DateField(verbose_name='Fecha de inicio')
    fecha_fin = models.DateField(verbose_name='Fecha de finalización')
    costo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Costo (S/.)')
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='Pendiente',
        verbose_name='Estado'
    )

    class Meta:
        db_table = 'tratamiento'
        verbose_name = 'Tratamiento'
        verbose_name_plural = 'Tratamientos'
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f'{self.nombre} - Diagnóstico #{self.diagnostico_id}'

