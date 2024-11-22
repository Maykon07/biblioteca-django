''' Desenvolvimento de Testes Automatizados
Desenvolva testes automatizados para a funcionalidade de coleções de livros. Assegure que os testes verifiquem:

1) Criação de uma nova coleção e associação correta ao usuário autenticado;

2)Permissões de acesso:
    Apenas o colecionador pode editar ou deletar sua coleção;
    Usuários não autenticados não podem criar, atualizar ou deletar coleções

3) Listagem de coleções visíveis para usuários autenticados'''

from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Colecao

class ColecaoTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_criar_colecao(self):
        url = '/api/colecoes/'
        data = {'nome': 'Minha Coleção'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Colecao.objects.count(), 1)
        self.assertEqual(Colecao.objects.get().colecionador, self.user)

    def test_apenas_colecionador_pode_editar_ou_deletar_colecao(self):
        colecao = Colecao.objects.create(nome='Minha Coleção', colecionador=self.user)
        url = f'/api/colecoes/{colecao.id}/'
        data = {'nome': 'Coleção Editada'}
        
        # Teste de edição pelo colecionador
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Colecao.objects.get().nome, 'Coleção Editada')
        
        # Teste de edição por outro usuário
        outro_usuario = User.objects.create_user(username='outro', password='testpass')
        self.client.force_authenticate(user=outro_usuario)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Teste de deleção pelo colecionador
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Colecao.objects.count(), 0)

    def test_usuario_nao_autenticado_nao_pode_criar_atualizar_ou_deletar_colecao(self):
        self.client.logout()
        url = '/api/colecoes/'
        data = {'nome': 'Minha Coleção'}
        
        # Teste de criação
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Teste de edição
        colecao = Colecao.objects.create(nome='Minha Coleção', colecionador=self.user)
        url = f'/api/colecoes/{colecao.id}/'
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Teste de deleção
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_listagem_colecoes_visiveis_para_usuarios_autenticados(self):
        Colecao.objects.create(nome='Coleção 1', colecionador=self.user)
        Colecao.objects.create(nome='Coleção 2', colecionador=self.user)
        
        url = '/api/colecoes/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)