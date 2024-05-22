from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from main.models import Project, Task, Tag  # ajuste para o nome correto do seu app
import json

class Command(BaseCommand):
    help = 'Loads data from JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', nargs='?', type=str, default='data.json', help='Path to the JSON file')

    def handle(self, *args, **options):
        try:
            with open(options['json_file'], 'r') as file:
                data = json.load(file)

            with transaction.atomic():
                User.objects.all().delete()
                for user_data in data['users']:
                    User.objects.create_user(username=user_data['username'], email=user_data['email'], password=user_data['password'])

                Tag.objects.all().delete()
                tags = [Tag.objects.create(title=tag_data['title']) for tag_data in data['tags']]

                Project.objects.all().delete()
                projects = [Project.objects.create(name=proj_data['name'], description=proj_data['description']) for proj_data in data['projects']]
                for project, proj_data in zip(projects, data['projects']):
                    member_users = User.objects.filter(username__in=proj_data['members_usernames'])
                    project.members.set(member_users)

                Task.objects.all().delete()
                for task_data in data['tasks']:
                    # Ajuste o índice de projeto para base-0
                    project_index = task_data['project'] - 1  # Subtrai 1 para converter índice base-1 para base-0
                    project = projects[project_index]
                    task = Task.objects.create(
                        title=task_data['title'],
                        description=task_data['description'],
                        status=task_data.get('status', 'P'),
                        project=project
                    )
                    task.tags.set([tags[tag_id - 1] for tag_id in task_data['tags']])  # Subtrai 1 aqui também se os índices de tags começam em 1
                    task.save()

        except Exception as e:
            self.stdout.write(self.style.ERROR('Erro ao carregar os dados: {}'.format(str(e))))
            raise e
