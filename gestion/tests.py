from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, time, timedelta
from decimal import Decimal
from gestion.models import (
    Especialidad, Paciente, Odontologo, Cita, Diagnostico, Tratamiento, Receta
)


class ModelosSonrisaPerfectaTest(TestCase):
    def setUp(self):
        self.esp = Especialidad.objects.create(
            nombre='Ortodoncia',
            descripcion='Tratamiento de alineación',
            estado='Activa'
        )
        self.pac = Paciente.objects.create(
            nombres='Carlos',
            apellidos='Santillán',
            dni='87654321',
            fecha_nacimiento=date(1990, 1, 1),
            telefono='999888777',
            direccion='Av. Arequipa 123',
            correo='carlos@correo.com'
        )
        self.odo = Odontologo.objects.create(
            nombres='Beatriz',
            apellidos='Luna',
            numero_colegiatura='COP-9988',
            telefono='988776655',
            correo='beatriz@correo.com',
            especialidad=self.esp,
            estado='Activo'
        )
        self.cita = Cita.objects.create(
            paciente=self.pac,
            odontologo=self.odo,
            fecha=date.today(),
            hora=time(10, 0),
            motivo='Revisión general',
            estado='Atendida',
            observaciones='Sin observaciones'
        )
        self.diag = Diagnostico.objects.create(
            cita=self.cita,
            descripcion='Caries de primer grado',
            recomendaciones='Curación simple',
            fecha=date.today()
        )
        self.trat = Tratamiento.objects.create(
            diagnostico=self.diag,
            nombre='Curación con resina',
            descripcion='Obturación fotopolimerizable',
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=1),
            costo=Decimal('120.00'),
            estado='En proceso'
        )
        self.receta = Receta.objects.create(
            diagnostico=self.diag,
            medicamento='Paracetamol 500mg',
            dosis='1 tableta',
            frecuencia='Cada 8 horas',
            duracion='2 días',
            indicaciones='Tomar tras alimentos',
            fecha_emision=date.today()
        )

    def test_creacion_siete_modelos(self):
        self.assertEqual(Especialidad.objects.count(), 1)
        self.assertEqual(Paciente.objects.count(), 1)
        self.assertEqual(Odontologo.objects.count(), 1)
        self.assertEqual(Cita.objects.count(), 1)
        self.assertEqual(Diagnostico.objects.count(), 1)
        self.assertEqual(Tratamiento.objects.count(), 1)
        self.assertEqual(Receta.objects.count(), 1)

    def test_metodos_str(self):
        self.assertEqual(str(self.esp), 'Ortodoncia')
        self.assertIn('Santillán', str(self.pac))
        self.assertIn('Luna', str(self.odo))
        self.assertIn('Cita', str(self.cita))
        self.assertIn('Diagnóstico', str(self.diag))
        self.assertIn('Curación con resina', str(self.trat))
        self.assertIn('Paracetamol', str(self.receta))


class AuthYVistasTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='doctor',
            password='Password123!',
            first_name='Juan',
            last_name='Pérez',
            email='doctor@clinica.pe'
        )
        self.esp = Especialidad.objects.create(
            nombre='Endodoncia',
            descripcion='Conductos',
            estado='Activa'
        )
        self.pac = Paciente.objects.create(
            nombres='Lucía',
            apellidos='Mendoza',
            dni='11223344',
            fecha_nacimiento=date(1995, 5, 20),
            telefono='911223344',
            direccion='Calle Lima 456',
            correo='lucia@correo.com'
        )
        self.odo = Odontologo.objects.create(
            nombres='Mario',
            apellidos='Vargas',
            numero_colegiatura='COP-5544',
            telefono='944556677',
            correo='mario@clinica.pe',
            especialidad=self.esp,
            estado='Activo'
        )
        self.cita = Cita.objects.create(
            paciente=self.pac,
            odontologo=self.odo,
            fecha=date.today(),
            hora=time(11, 30),
            motivo='Dolor dental',
            estado='Atendida'
        )
        self.diag = Diagnostico.objects.create(
            cita=self.cita,
            descripcion='Pulpitis aguda',
            recomendaciones='Endodoncia unirradicular',
            fecha=date.today()
        )
        self.trat = Tratamiento.objects.create(
            diagnostico=self.diag,
            nombre='Tratamiento de conducto',
            descripcion='Instrumentación rotatoria',
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=3),
            costo=Decimal('350.00'),
            estado='En proceso'
        )
        self.receta = Receta.objects.create(
            diagnostico=self.diag,
            medicamento='Ketorolaco 10mg',
            dosis='1 tableta sublingual',
            frecuencia='Cada 8 horas',
            duracion='3 días',
            indicaciones='Solo si persiste dolor',
            fecha_emision=date.today()
        )

    def test_login_exitoso_y_checkbox_recordar(self):
        # Login con remember_me = True (sesión persistente)
        response = self.client.post(reverse('login'), {
            'username': 'doctor',
            'password': 'Password123!',
            'remember_me': 'on',
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.client.session.get_expire_at_browser_close())
        self.assertEqual(self.client.session.get_expiry_age(), 1209600)

        # Logout
        self.client.get(reverse('logout'))

        # Login con remember_me = False (sesión expira al cerrar navegador)
        response2 = self.client.post(reverse('login'), {
            'username': 'doctor',
            'password': 'Password123!',
        })
        self.assertEqual(response2.status_code, 302)
        self.assertTrue(self.client.session.get_expire_at_browser_close())

    def test_registro_usuario(self):
        response = self.client.post(reverse('registro'), {
            'username': 'asistente',
            'first_name': 'María',
            'last_name': 'García',
            'email': 'asistente@clinica.pe',
            'password': 'Password123!',
            'password_confirm': 'Password123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='asistente').exists())

    def test_dashboard_indicadores(self):
        self.client.login(username='doctor', password='Password123!')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
        self.assertIn('total_pacientes', response.context)
        self.assertIn('total_citas', response.context)
        self.assertIn('total_tratamientos', response.context)
        self.assertIn('total_diagnosticos', response.context)

    def test_crud_paciente(self):
        self.client.login(username='doctor', password='Password123!')
        # Listar y buscar
        resp = self.client.get(reverse('paciente_lista') + '?q=Lucía')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Mendoza')

        # Detalle
        resp_det = self.client.get(reverse('paciente_detalle', args=[self.pac.pk]))
        self.assertEqual(resp_det.status_code, 200)

        # Crear
        resp_post = self.client.post(reverse('paciente_crear'), {
            'nombres': 'Pedro',
            'apellidos': 'Suárez',
            'dni': '99887766',
            'fecha_nacimiento': '1998-07-15',
            'telefono': '987123456',
            'direccion': 'Av. Grau 555',
            'correo': 'pedro@correo.com'
        })
        self.assertEqual(resp_post.status_code, 302)
        self.assertTrue(Paciente.objects.filter(dni='99887766').exists())

        # Editar
        p = Paciente.objects.get(dni='99887766')
        self.client.post(reverse('paciente_editar', args=[p.pk]), {
            'nombres': 'Pedro Antonio',
            'apellidos': 'Suárez',
            'dni': '99887766',
            'fecha_nacimiento': '1998-07-15',
            'telefono': '987123456',
            'direccion': 'Av. Grau 555 Int 2',
            'correo': 'pedro@correo.com'
        })
        p.refresh_from_db()
        self.assertEqual(p.nombres, 'Pedro Antonio')

        # Eliminar
        resp_del = self.client.post(reverse('paciente_eliminar', args=[p.pk]))
        self.assertEqual(resp_del.status_code, 302)
        self.assertFalse(Paciente.objects.filter(pk=p.pk).exists())

    def test_reportes_pdf_y_filtros(self):
        self.client.login(username='doctor', password='Password123!')

        # PDF Citas
        resp_citas = self.client.get(reverse('cita_reporte_pdf') + '?estado=Atendida')
        self.assertEqual(resp_citas.status_code, 200)
        self.assertEqual(resp_citas['Content-Type'], 'application/pdf')

        # PDF Diagnósticos
        resp_diag = self.client.get(reverse('diagnostico_reporte_pdf'))
        self.assertEqual(resp_diag.status_code, 200)
        self.assertEqual(resp_diag['Content-Type'], 'application/pdf')

        # PDF Tratamientos
        resp_trat = self.client.get(reverse('tratamiento_reporte_pdf') + '?estado=En proceso')
        self.assertEqual(resp_trat.status_code, 200)
        self.assertEqual(resp_trat['Content-Type'], 'application/pdf')

        # PDF Recetas
        resp_rec = self.client.get(reverse('receta_reporte_pdf'))
        self.assertEqual(resp_rec.status_code, 200)
        self.assertEqual(resp_rec['Content-Type'], 'application/pdf')

        # Centro de Reportes
        resp_centro = self.client.get(reverse('reportes_centro'))
        self.assertEqual(resp_centro.status_code, 200)

        # PDF Receta Individual Oficial
        resp_rec_ind = self.client.get(reverse('receta_individual_pdf', args=[self.receta.pk]))
        self.assertEqual(resp_rec_ind.status_code, 200)
        self.assertEqual(resp_rec_ind['Content-Type'], 'application/pdf')
