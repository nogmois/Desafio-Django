from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from .models import Project
import json

class ProjectTests(TestCase):
    """Testes relacionados à criação de projetos no sistema."""

    def setUp(self):
        # Configuração inicial para criar e logar o usuário antes de cada teste.
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_create_project(self):
        # Testa a criação de um novo projeto via POST.
        data = {
            'name': 'New Project',
            'description': 'Test Project'
        }
        response = self.client.post('/api/projects/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ProjectPermissionsTest(TestCase):
    """Testes para verificar as permissões de modificação de projetos por diferentes usuários."""

    def setUp(self):
        # Configuração inicial criando dois usuários e um projeto.
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.project = Project.objects.create(name='Test Project', creator=self.user1)
        self.update_url = f'/api/projects/{self.project.id}/'

    def test_project_modification_by_creator(self):
        # Testa se o criador do projeto pode modificar o projeto.
        self.client.login(username='user1', password='pass1')
        data = json.dumps({'name': 'New Name'})
        response = self.client.patch(self.update_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_project_modification_by_non_creator(self):
        # Testa se um usuário que não é o criador não pode modificar o projeto.
        self.client.login(username='user2', password='pass2')
        data = json.dumps({'name': 'New Name'})
        response = self.client.patch(self.update_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 403)

class ProjectDeletionTest(TestCase):
    """Testes para verificar as permissões de exclusão de projetos por diferentes usuários."""

    def setUp(self):
        # Configuração inicial criando dois usuários e um projeto deletável.
        self.user1 = User.objects.create_user(username='creator', password='password')
        self.user2 = User.objects.create_user(username='noncreator', password='password')
        self.project = Project.objects.create(name='Deletable Project', description='To be deleted', creator=self.user1)

    def test_delete_project_by_creator(self):
        # Testa se o criador do projeto pode deletá-lo.
        self.client.login(username='creator', password='password')
        response = self.client.delete(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_project_by_non_creator(self):
        # Testa se um usuário que não é o criador não pode deletar o projeto.
        self.client.login(username='noncreator', password='password')
        response = self.client.delete(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TaskCreationTest(TestCase):
    """Testes relacionados à criação de tarefas dentro de um projeto por membros e não membros."""

    def setUp(self):
        # Configuração inicial criando usuários e um projeto com membros.
        self.user1 = User.objects.create_user(username='taskcreator', password='password')
        self.user2 = User.objects.create_user(username='outsider', password='password')
        self.project = Project.objects.create(name='Task Project', description='Tasks added here', creator=self.user1)
        self.project.members.add(self.user1)

    def test_add_task_by_member(self):
        # Testa se um membro do projeto pode adicionar tarefas.
        self.client.login(username='taskcreator', password='password')
        data = json.dumps({'title': 'New Task', 'description': 'Do something important', 'project': self.project.id})
        response = self.client.post(f'/api/projects/{self.project.id}/tasks/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_task_by_non_member(self):
        # Testa se um não membro não pode adicionar tarefas.
        self.client.login(username='outsider', password='password')
        data = json.dumps({'title': 'Unauthorized Task', 'description': 'Should not be added', 'project': self.project.id})
        response = self.client.post(f'/api/projects/{self.project.id}/tasks/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
