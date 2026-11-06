from django.db import models
from gestion.models.diagnostico import Diagnostico


class Receta(models.Model):
    diagnostico = models.ForeignKey(
        Diagnostico,
        on_delete=models.PROTECT,
        related_name='recetas',
        verbose_name='Diagnóstico'
    )
    medicamento = models.CharField(max_length=150, verbose_name='Medicamento')
    dosis = models.CharField(max_length=100, verbose_name='Dosis')
    frecuencia = models.CharField(max_length=100, verbose_name='Frecuencia')
    duracion = models.CharField(max_length=100, verbose_name='Duración')
    indicaciones = models.TextField(verbose_name='Indicaciones adicionales')
    fecha_emision = models.DateField(verbose_name='Fecha de emisión')

    class Meta:
        db_table = 'receta'
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'
        ordering = ['-fecha_emision']

    def __str__(self):
        return f'{self.medicamento} - Diagnóstico #{self.diagnostico_id}'

