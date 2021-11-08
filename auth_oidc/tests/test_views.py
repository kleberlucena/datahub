from django.test import TestCase
from django.test import Client
from django.urls import reverse_lazy


class LogoutTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_not_authenticated_logout(self):
        '''
        Test of redirect on logout
        '''
        request = self.client.get(reverse_lazy('auth_oidc:logout'))
        self.assertEqual(request.status_code, 302)