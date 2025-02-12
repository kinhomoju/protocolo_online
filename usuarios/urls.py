from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_usuario, name='login'),
    path('pesquisa_usuarios/', views.pesquisa_usuarios, name='pesquisa_usuarios'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard_master/', views.dashboard_master, name='dashboard_master'),
    path('aprovar/', views.aprovar_usuarios, name='aprovar_usuarios'),
    path('excluir/', views.excluir_usuarios, name='excluir_usuarios'),
    path('excluir_usuario/<int:user_id>/', views.excluir_usuarios, name='excluir_usuario'),
    path('completar_cadastro/', views.completar_cadastro, name='completar_cadastro'),
    path('logout/', views.logout_usuario, name='logout'),
    path('nao_aprovado/', views.nao_aprovado, name='nao_aprovado'),
]
