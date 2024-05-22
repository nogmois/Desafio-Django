from rest_framework import viewsets, permissions
from .models import Project, Task, Tag
from .serializers import ProjectSerializer, TaskSerializer, TagSerializer
from .permissions import IsProjectOwner
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectOwner]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
from rest_framework.exceptions import PermissionDenied


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        if self.request.user not in project.members.all():
            raise PermissionDenied("You do not have permission to add tasks to this project.")
        serializer.save()


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]





def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Debug: username={username}, password={password}")  # Adicionado para debug
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            tokens = get_tokens_for_user(user)
            return render(request, 'api_access.html', {'tokens': tokens})
        else:
            print("Debug: Invalid login")  # Adicionado para debug
            return HttpResponse("Invalid login", status=401)
    else:
        return render(request, 'login.html')