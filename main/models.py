from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

# Modelo para representar um projeto, com um criador (usuário), nome, descrição e membros.
class Project(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_projects', null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='projects')

    def __str__(self):
        return self.name

# Modelo para representar uma tarefa, com título, descrição, data de criação, status, projeto associado e tags.
class Task(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('E', 'Em andamento'),
        ('C', 'Concluída')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    tags = models.ManyToManyField('Tag', related_name='tasks')

    def __str__(self):
        return self.title
    
# Modelo para representar uma tag, com título.
class Tag(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title