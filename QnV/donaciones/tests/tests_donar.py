from django.test import TestCase, RequestFactory
from donaciones.views import donar
from django.contrib.auth import get_user_model


class DonarTests(TestCase):
    def setUp(self):


        self.user = get_user_model().objects.create_superuser(
            email='superuser@example.com',
            username='superuser',
            password='secret',
        )
        super(DonarTests, self).setUp()

    def test_medicamento_existe_entonces_se_guarda_nueva_donacion_con_med_existente(self):


            
        f = RequestFactory()
        test_request = f.post('xxx', {'donar_nombre': 'TAFIROL',
                                      'donar_concentracion_gramos': '500',
                                      'donar_cantidad' : '10',
                                      'donar_laboratorio': 'GENOMMA',
                                      'donar_fecha_vencimiento' : '2018-05-21',
                                      'donar_tipo': 'Pastillas',
                                      'donar_droga': 'PARACETAMOL',
                                      'author': 'username',
                                      })
        test_request.user = self.user
        donar(test_request)
        self.assertTrue(False)
    #def test_medicamento_existe_no_se_crea_nuevo_med(self):
    #   pass

    #def test_medicamento_existe_devuelve_redirect_a_main(self):
    #   pass

    #def test_medicamento_no_existe_entonces_xx(self):
        # 1) nuevo med en DB
        # 2) nueva don en bd con referencia al nuevo med
    #   pass


#class GuardarDonacionTests(TestCase):
#   pass
