from django.urls import path
from gestion import views

urlpatterns = [
    # Raíz → dashboard
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard_home'),

    # Centro de Reportes
    path('reportes/', views.reportes_centro, name='reportes_centro'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),

    # Especialidades
    path('especialidades/', views.especialidad_lista, name='especialidad_lista'),
    path('especialidades/nuevo/', views.especialidad_crear, name='especialidad_crear'),
    path('especialidades/<int:pk>/editar/', views.especialidad_editar, name='especialidad_editar'),
    path('especialidades/<int:pk>/eliminar/', views.especialidad_eliminar, name='especialidad_eliminar'),

    # Pacientes
    path('pacientes/', views.paciente_lista, name='paciente_lista'),
    path('pacientes/nuevo/', views.paciente_crear, name='paciente_crear'),
    path('pacientes/<int:pk>/', views.paciente_detalle, name='paciente_detalle'),
    path('pacientes/<int:pk>/editar/', views.paciente_editar, name='paciente_editar'),
    path('pacientes/<int:pk>/eliminar/', views.paciente_eliminar, name='paciente_eliminar'),

    # Odontólogos
    path('odontologos/', views.odontologo_lista, name='odontologo_lista'),
    path('odontologos/nuevo/', views.odontologo_crear, name='odontologo_crear'),
    path('odontologos/<int:pk>/editar/', views.odontologo_editar, name='odontologo_editar'),
    path('odontologos/<int:pk>/eliminar/', views.odontologo_eliminar, name='odontologo_eliminar'),

    # Citas
    path('citas/', views.cita_lista, name='cita_lista'),
    path('citas/nueva/', views.cita_crear, name='cita_crear'),
    path('citas/<int:pk>/editar/', views.cita_editar, name='cita_editar'),
    path('citas/<int:pk>/eliminar/', views.cita_eliminar, name='cita_eliminar'),
    path('citas/reporte/pdf/', views.cita_reporte_pdf, name='cita_reporte_pdf'),

    # Diagnósticos
    path('diagnosticos/', views.diagnostico_lista, name='diagnostico_lista'),
    path('diagnosticos/nuevo/', views.diagnostico_crear, name='diagnostico_crear'),
    path('diagnosticos/<int:pk>/editar/', views.diagnostico_editar, name='diagnostico_editar'),
    path('diagnosticos/<int:pk>/eliminar/', views.diagnostico_eliminar, name='diagnostico_eliminar'),
    path('diagnosticos/reporte/pdf/', views.diagnostico_reporte_pdf, name='diagnostico_reporte_pdf'),

    # Tratamientos
    path('tratamientos/', views.tratamiento_lista, name='tratamiento_lista'),
    path('tratamientos/nuevo/', views.tratamiento_crear, name='tratamiento_crear'),
    path('tratamientos/<int:pk>/editar/', views.tratamiento_editar, name='tratamiento_editar'),
    path('tratamientos/<int:pk>/eliminar/', views.tratamiento_eliminar, name='tratamiento_eliminar'),
    path('tratamientos/reporte/pdf/', views.tratamiento_reporte_pdf, name='tratamiento_reporte_pdf'),

    # Recetas
    path('recetas/', views.receta_lista, name='receta_lista'),
    path('recetas/nueva/', views.receta_crear, name='receta_crear'),
    path('recetas/<int:pk>/editar/', views.receta_editar, name='receta_editar'),
    path('recetas/<int:pk>/eliminar/', views.receta_eliminar, name='receta_eliminar'),
    path('recetas/reporte/pdf/', views.receta_reporte_pdf, name='receta_reporte_pdf'),
    path('recetas/<int:pk>/pdf/', views.receta_individual_pdf, name='receta_individual_pdf'),
]
