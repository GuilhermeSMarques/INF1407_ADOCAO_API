from rest_framework import status
from rest_framework.test import APITestCase

from usuarios.models import Usuario

from .models import Pet


class PetsAPITestCase(APITestCase):
    def setUp(self):
        self.responsavel = Usuario.objects.create_user(
            email='responsavel@example.com',
            password='senhaTeste123',
            nome='Responsavel',
            tipo_usuario='responsavel',
        )
        self.outro_responsavel = Usuario.objects.create_user(
            email='outro@example.com',
            password='senhaTeste123',
            nome='Outro Responsavel',
            tipo_usuario='responsavel',
        )
        self.adotante = Usuario.objects.create_user(
            email='adotante@example.com',
            password='senhaTeste123',
            nome='Adotante',
        )

    def autenticar(self, usuario):
        self.client.force_authenticate(user=usuario)

    def test_responsavel_cria_e_edita_apenas_proprio_pet(self):
        self.autenticar(self.responsavel)
        resposta = self.client.post('/api/pets/', {
            'nome': 'Luna',
            'especie': Pet.Especie.GATO,
            'porte': Pet.Porte.PEQUENO,
        }, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        pet_id = resposta.data['id']

        self.autenticar(self.outro_responsavel)
        resposta_outro = self.client.patch(f'/api/pets/{pet_id}/', {'nome': 'Nome indevido'}, format='json')
        self.assertEqual(resposta_outro.status_code, status.HTTP_404_NOT_FOUND)

        self.autenticar(self.responsavel)
        resposta_dono = self.client.patch(f'/api/pets/{pet_id}/', {'nome': 'Luna Atualizada'}, format='json')
        self.assertEqual(resposta_dono.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta_dono.data['nome'], 'Luna Atualizada')

    def test_adotante_lista_disponiveis_mas_nao_cria_pet(self):
        Pet.objects.create(
            nome='Teca',
            especie=Pet.Especie.CACHORRO,
            porte=Pet.Porte.MEDIO,
            responsavel=self.responsavel,
        )

        self.autenticar(self.adotante)
        listagem = self.client.get('/api/pets/')
        criacao = self.client.post('/api/pets/', {
            'nome': 'Pet indevido',
            'especie': Pet.Especie.GATO,
            'porte': Pet.Porte.PEQUENO,
        }, format='json')

        self.assertEqual(listagem.status_code, status.HTTP_200_OK)
        self.assertEqual(len(listagem.data), 1)
        self.assertEqual(criacao.status_code, status.HTTP_403_FORBIDDEN)