from django.test import TestCase
from django.test import Client
import unittest
# Create your tests here.


class TestUno(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def testRedirect(self):
        response = self.client.post('/home')
        self.assertEqual(response.status_code, 302)

    def testRedirectChain(self):  # if not logged
        response = self.client.post('/home', follow=True)
        self.assertEqual(len(response.redirect_chain), 1)
