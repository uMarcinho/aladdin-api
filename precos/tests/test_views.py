from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.urls import reverse
import requests


class PrecosViewTest(TestCase):

    def test_sem_parametro_data_retorna_400(self):
        response = self.client.get('/api/precos/')
        self.assertEqual(response.status_code, 400)
        self.assertIn('erro', response.json())

    @patch('precos.views.requests.get')
    def test_retorno_com_sucesso(self, mock_get):
        # simula a resposta da API externa
        mock_resposta = MagicMock()
        mock_resposta.json.return_value = [{"tapete": "Persa", "preco": 500.0}]
        mock_resposta.raise_for_status.return_value = None
        mock_get.return_value = mock_resposta

        response = self.client.get('/api/precos/?data=2025-06-01')

        self.assertEqual(response.status_code, 200)
        dados = response.json()
        self.assertEqual(dados['data_consulta'], '2025-06-01')
        self.assertIn('precos', dados)
        self.assertEqual(len(dados['precos']), 1)

    @patch('precos.views.requests.get')
    def test_api_externa_fora_do_ar_retorna_502(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError

        response = self.client.get('/api/precos/?data=2025-06-01')

        self.assertEqual(response.status_code, 502)
        self.assertIn('erro', response.json())

    @patch('precos.views.requests.get')
    def test_timeout_retorna_502(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout

        response = self.client.get('/api/precos/?data=2025-06-01')

        self.assertEqual(response.status_code, 502)
        self.assertIn('erro', response.json())
