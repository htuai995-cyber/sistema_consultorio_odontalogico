from django.db import models
from gestion.models.paciente import Paciente
from gestion.models.odontologo import Odontologo


class Cita(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Atendida', 'Atendida'),
        ('Cancelada', 'Cancelada'),
    ]

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.PROTECT,
        related_name='citas',
        verbose_name='Paciente'
    )
    odontologo = models.ForeignKey(
        Odontologo,
        on_delete=models.PROTECT,
        related_name='citas',
        verbose_name='Odontólogo'
    )
    fecha = models.DateField(verbose_name='Fecha de atención')
    hora = models.TimeField(verbose_name='Hora de atención')
    motivo = models.CharField(max_length=200, verbose_name='Motivo de consulta')
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='Pendiente',
        verbose_name='Estado'
    )
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')

    class Meta:
        db_table = 'cita'
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['-fecha', '-hora']

    def __str__(self):
        return f'Cita {self.id} - {self.paciente} ({self.fecha})'

