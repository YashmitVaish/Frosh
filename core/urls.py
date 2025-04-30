from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rules/', views.rules, name='rules'),
    path('register/', views.register, name='register'),
    path('post_login/', views.post_login, name='post_login'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('question/', views.question, name='question'),
    path('admin-panel/', views.admin_page, name='admin_page'),
    path('questions/', views.question_list, name='question_list'),
    path('questions/add/', views.add_question, name='add_question'),
    path('questions/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('questions/<int:question_id>/delete/', views.delete_question, name='delete_question'),
]