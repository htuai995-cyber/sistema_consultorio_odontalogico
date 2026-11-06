from django.db import models
from gestion.models.cita import Cita


class Diagnostico(models.Model):
    cita = models.ForeignKey(
        Cita,
        on_delete=models.PROTECT,
        related_name='diagnosticos',
        verbose_name='Cita'
    )
    descripcion = models.TextField(verbose_name='Diagnóstico clínico')
    recomendaciones = models.TextField(verbose_name='Recomendaciones')
    fecha = models.DateField(verbose_name='Fecha del diagnóstico')

    class Meta:
        db_table = 'diagnostico'
        verbose_name = 'Diagnóstico'
        verbose_name_plural = 'Diagnósticos'
        ordering = ['-fecha']

    def __str__(self):
        return f'Diagnóstico #{self.id} - Cita #{self.cita_id}'

