from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'subtasks', views.SubTaskViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/chat/history/', views.chat_history, name='chat_history'),
    path('api/chat/clear/', views.clear_chat, name='clear_chat'),
]
