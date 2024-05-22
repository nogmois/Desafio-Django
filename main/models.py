from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class Project(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_projects', null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='projects')

    def __str__(self):
        return self.name


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
    

class Tag(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title