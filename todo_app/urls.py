from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'subtasks', views.SubTaskViewSet)
router.register(r'attachments', views.AttachmentViewSet)

urlpatterns = [
    path('', views.landing_page, name='home'),
    path('app/', views.index, name='app'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('api/', include(router.urls)),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/chat/history/', views.chat_history, name='chat_history'),
    path('api/chat/clear/', views.clear_chat, name='clear_chat'),
    path('api/auth/csrf/', views.auth_csrf, name='auth_csrf'),
    path('api/auth/status/', views.auth_status, name='auth_status'),
    path('api/auth/signup/', views.auth_signup, name='auth_signup'),
    path('api/auth/login/', views.auth_login, name='auth_login'),
    path('api/auth/logout/', views.auth_logout, name='auth_logout'),
]
