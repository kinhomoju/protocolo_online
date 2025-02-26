from django.urls import path
from . import views

app_name = 'protocolos'

urlpatterns = [
    path('lancar/', views.lancar_protocolo, name='lancar_protocolo'),
    path('comprovante/<int:protocolo_id>/', views.comprovante_protocolo, name='comprovante'),
    path('visualizar/<int:protocolo_id>/', views.visualizar_protocolo, name='visualizar_protocolo'),
    path('pesquisa/', views.pesquisa_protocolos, name='pesquisa_protocolos'),
    path('editar/<int:protocolo_id>/', views.editar_protocolo, name='editar_protocolo'),
    path('excluir/<int:protocolo_id>/', views.excluir_protocolo, name='excluir_protocolo'),
]
