from rest_framework import status
from rest_framework.test import APITestCase

from pets.models import Pet
from usuarios.models import Usuario

from .models import Favorito, SolicitacaoAdocao


class AdocoesAPITestCase(APITestCase):
    def setUp(self):
        self.adotante_a = Usuario.objects.create_user(
            email='adotante.a@example.com',
            password='senhaTeste123',
            nome='Adotante A',
        )
        self.adotante_b = Usuario.objects.create_user(
            email='adotante.b@example.com',
            password='senhaTeste123',
            nome='Adotante B',
        )
        self.responsavel_a = Usuario.objects.create_user(
            email='responsavel.a@example.com',
            password='senhaTeste123',
            nome='Responsavel A',
            tipo_usuario='responsavel',
        )
        self.responsavel_b = Usuario.objects.create_user(
            email='responsavel.b@example.com',
            password='senhaTeste123',
            nome='Responsavel B',
            tipo_usuario='responsavel',
        )
        self.pet_a = Pet.objects.create(
            nome='Bento',
            especie=Pet.Especie.CACHORRO,
            porte=Pet.Porte.MEDIO,
            responsavel=self.responsavel_a,
        )
        self.pet_b = Pet.objects.create(
            nome='Mia',
            especie=Pet.Especie.GATO,
            porte=Pet.Porte.PEQUENO,
            responsavel=self.responsavel_b,
        )

    def autenticar(self, usuario):
        self.client.force_authenticate(user=usuario)

    def test_solicitacoes_tem_visao_por_usuario_e_responsavel(self):
        solicitacao = SolicitacaoAdocao.objects.create(usuario=self.adotante_a, pet=self.pet_a)

        self.autenticar(self.adotante_a)
        resposta_adotante_a = self.client.get('/api/solicitacoes/')
        self.assertEqual(len(resposta_adotante_a.data), 1)

        self.autenticar(self.adotante_b)
        resposta_adotante_b = self.client.get('/api/solicitacoes/')
        self.assertEqual(len(resposta_adotante_b.data), 0)

        self.autenticar(self.responsavel_a)
        resposta_responsavel_a = self.client.get('/api/solicitacoes/')
        self.assertEqual(len(resposta_responsavel_a.data), 1)

        self.autenticar(self.responsavel_b)
        resposta_responsavel_b = self.client.get('/api/solicitacoes/')
        self.assertEqual(len(resposta_responsavel_b.data), 0)

        self.autenticar(self.responsavel_a)
        aprovar = self.client.post(f'/api/solicitacoes/{solicitacao.id}/aprovar/')
        self.pet_a.refresh_from_db()

        self.assertEqual(aprovar.status_code, status.HTTP_200_OK)
        self.assertEqual(aprovar.data['status'], SolicitacaoAdocao.Status.APROVADA)
        self.assertEqual(self.pet_a.status, Pet.Status.ADOTADO)

    def test_favoritos_tem_visao_por_usuario(self):
        Favorito.objects.create(usuario=self.adotante_a, pet=self.pet_a)

        self.autenticar(self.adotante_a)
        resposta_a = self.client.get('/api/favoritos/')
        self.assertEqual(resposta_a.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta_a.data), 1)

        self.autenticar(self.adotante_b)
        resposta_b = self.client.get('/api/favoritos/')
        self.assertEqual(resposta_b.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta_b.data), 0)

    def test_dashboard_retorna_dados_diferentes_por_usuario(self):
        SolicitacaoAdocao.objects.create(usuario=self.adotante_a, pet=self.pet_a)
        Favorito.objects.create(usuario=self.adotante_a, pet=self.pet_b)

        self.autenticar(self.adotante_a)
        dashboard_adotante = self.client.get('/api/dashboard/')

        self.autenticar(self.responsavel_a)
        dashboard_responsavel_a = self.client.get('/api/dashboard/')

        self.autenticar(self.responsavel_b)
        dashboard_responsavel_b = self.client.get('/api/dashboard/')

        self.assertEqual(dashboard_adotante.data['favoritos'], 1)
        self.assertEqual(dashboard_adotante.data['solicitacoes_pendentes'], 1)
        self.assertEqual(dashboard_responsavel_a.data['solicitacoes_pendentes'], 1)
        self.assertEqual(dashboard_responsavel_b.data['solicitacoes_pendentes'], 0)