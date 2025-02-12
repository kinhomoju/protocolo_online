from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import transaction
from .models import Protocolo
from .forms import ProtocoloForm
from django.utils import timezone

def gerar_numero_protocolo():
    now = timezone.localtime(timezone.now())
    date_prefix = now.strftime('%d%m%Y')
    time_part = now.strftime('%H%M%S')
    # Conta os protocolos criados hoje
    count = Protocolo.objects.filter(numero__startswith=date_prefix).count() + 1
    sequence = str(count).zfill(4)
    return date_prefix + time_part + sequence

@login_required
def lancar_protocolo(request):
    """
    Cria um novo protocolo automaticamente e redireciona para a tela de visualização,
    onde o protocolo recém-criado (com número gerado automaticamente) é exibido.
    """
    provisional_number = gerar_numero_protocolo()
    
    if request.method == 'POST':
        form = ProtocoloForm(request.POST)
        if form.is_valid():
            protocolo = form.save(commit=False)
            # Use o número passado no campo oculto ou re-gere se necessário
            protocolo.numero = request.POST.get('numero_protocolo', provisional_number)
            protocolo.usuario = request.user
            # Salva o protocolo com a transação para garantir a unicidade
            protocolo.save()
            messages.success(request, f"Protocolo {protocolo.numero} salvo com sucesso.")
            return redirect('protocolos:comprovante', protocolo_id=protocolo.id)
    else:
        form = ProtocoloForm()
    
    return render(request, 'protocolos/lancar_protocolo.html', {
        'form': form,
        'protocolo_numero': provisional_number,
    })

@login_required
def visualizar_protocolo(request, protocolo_id):
    """
    Exibe uma página com os detalhes do protocolo recém-criado.
    O número do protocolo é exibido e não pode ser editado.
    """
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    return render(request, 'protocolos/visualizar_protocolo.html', {'protocolo': protocolo})

@login_required
def pesquisa_protocolos(request):
    """
    View para pesquisar protocolos com base no número ou descrição.
    """
    query = request.GET.get('q', '')
    if query:
        # Pesquisa: filtra por número ou descrição
        protocolos_pesquisa = Protocolo.objects.filter(
            Q(numero__icontains=query) | Q(descricao__icontains=query)
        )
        context = {
            'protocolos_pesquisa': protocolos_pesquisa,
            'query': query,
        }
    else:
        # Sem pesquisa: exibe os protocolos lançados pelo usuário com paginação
        protocolos = Protocolo.objects.filter(usuario=request.user).order_by('-data_criacao')
        paginator = Paginator(protocolos, 10)
        page_number = request.GET.get('page')
        protocolos_recent = paginator.get_page(page_number)
        context = {
            'protocolos_recent': protocolos_recent,
        }
    return render(request, 'protocolos/pesquisa_protocolos.html', context)

@login_required
def editar_protocolo(request, protocolo_id):
    """
    View para editar (corrigir) um protocolo, se o status permitir.
    """
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    # Se o protocolo já estiver em status final, pode impedir a edição (opcional)
    if request.method == 'POST':
        form = ProtocoloForm(request.POST, instance=protocolo)
        if form.is_valid():
            form.save()
            messages.success(request, "Protocolo atualizado com sucesso.")
            return redirect('protocolos:pesquisa_protocolos')
    else:
        form = ProtocoloForm(instance=protocolo)
    return render(request, 'protocolos/editar_protocolo.html', {'form': form, 'protocolo': protocolo})

@login_required
def excluir_protocolo(request, protocolo_id):
    """
    View para excluir um protocolo se o status permitir.
    """
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    # Verifique se o protocolo pode ser excluído (opcional, por status)
    if protocolo.status in ['pago', 'rejeitado', 'devolvido']:
        messages.error(request, "Este protocolo não pode ser excluído.")
        return redirect('protocolos:pesquisa_protocolos')
    
    if request.method == 'POST':
        protocolo.delete()
        messages.success(request, "Protocolo excluído com sucesso.")
        return redirect('protocolos:pesquisa_protocolos')
    
    return render(request, 'protocolos/confirmar_exclusao.html', {'protocolo': protocolo})

@login_required
def comprovante_protocolo(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    return render(request, 'protocolos/comprovante_protocolo.html', {'protocolo': protocolo})
