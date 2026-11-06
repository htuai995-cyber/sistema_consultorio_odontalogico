from gestion.views.dashboard_views import dashboard
from gestion.views.auth_views import login_view, logout_view, registro_view
from gestion.views.especialidad_views import (
    especialidad_lista, especialidad_crear, especialidad_editar, especialidad_eliminar
)
from gestion.views.paciente_views import (
    paciente_lista, paciente_crear, paciente_editar, paciente_eliminar, paciente_detalle
)
from gestion.views.odontologo_views import (
    odontologo_lista, odontologo_crear, odontologo_editar, odontologo_eliminar
)
from gestion.views.cita_views import (
    cita_lista, cita_crear, cita_editar, cita_eliminar, cita_reporte_pdf
)
from gestion.views.diagnostico_views import (
    diagnostico_lista, diagnostico_crear, diagnostico_editar, diagnostico_eliminar, diagnostico_reporte_pdf
)
from gestion.views.tratamiento_views import (
    tratamiento_lista, tratamiento_crear, tratamiento_editar, tratamiento_eliminar, tratamiento_reporte_pdf
)
from gestion.views.receta_views import (
    receta_lista, receta_crear, receta_editar, receta_eliminar, receta_reporte_pdf
)
from gestion.views.reportes_views import reportes_centro, receta_individual_pdf

__all__ = [
    'dashboard',
    'login_view', 'logout_view', 'registro_view',
    'especialidad_lista', 'especialidad_crear', 'especialidad_editar', 'especialidad_eliminar',
    'paciente_lista', 'paciente_crear', 'paciente_editar', 'paciente_eliminar', 'paciente_detalle',
    'odontologo_lista', 'odontologo_crear', 'odontologo_editar', 'odontologo_eliminar',
    'cita_lista', 'cita_crear', 'cita_editar', 'cita_eliminar', 'cita_reporte_pdf',
    'diagnostico_lista', 'diagnostico_crear', 'diagnostico_editar', 'diagnostico_eliminar', 'diagnostico_reporte_pdf',
    'tratamiento_lista', 'tratamiento_crear', 'tratamiento_editar', 'tratamiento_eliminar', 'tratamiento_reporte_pdf',
    'receta_lista', 'receta_crear', 'receta_editar', 'receta_eliminar', 'receta_reporte_pdf',
    'reportes_centro', 'receta_individual_pdf',
]
