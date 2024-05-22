from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet, TagViewSet
from .views import login_view


router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'tags', TagViewSet)
router.register(r'projects/(?P<project_pk>[^/.]+)/tasks', TaskViewSet, basename='project-tasks')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view, name='login'),
]
