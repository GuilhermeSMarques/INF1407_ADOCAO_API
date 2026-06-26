from rest_framework import status
from rest_framework.test import APITestCase


class AutenticacaoAPITestCase(APITestCase):
    def test_cadastro_login_e_usuario_atual(self):
        cadastro = self.client.post('/api/auth/register/', {
            'nome': 'Usuario Teste',
            'email': 'usuario@example.com',
            'telefone': '21999999999',
            'tipo_usuario': 'adotante',
            'senha': 'senhaTeste123',
        }, format='json')

        self.assertEqual(cadastro.status_code, status.HTTP_201_CREATED)
        self.assertEqual(cadastro.data['email'], 'usuario@example.com')

        login = self.client.post('/api/auth/login/', {
            'email': 'usuario@example.com',
            'password': 'senhaTeste123',
        }, format='json')

        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.assertIn('access', login.data)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {login.data["access"]}')
        usuario_atual = self.client.get('/api/auth/me/')

        self.assertEqual(usuario_atual.status_code, status.HTTP_200_OK)
        self.assertEqual(usuario_atual.data['email'], 'usuario@example.com')