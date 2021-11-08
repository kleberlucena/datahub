from django.test import TestCase
from django.test import Client
from django.urls import reverse_lazy


class HealtCheckTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_requisition_get(self):
        request = self.client.get(reverse_lazy('base:health_check'))
        self.assertEqual(request.status_code, 204)