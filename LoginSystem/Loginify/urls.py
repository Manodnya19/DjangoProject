from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('get_all_users/', views.get_all_users, name='get_all_users'),
    path('get_user/', views.get_user_by_email, name='get_user'),
    path('update_user/', views.update_user, name='update_user'),
    path('delete_user/', views.delete_user, name='delete_user'),
]
