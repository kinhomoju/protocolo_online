from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import transaction
from django.utils import timezone
from django.forms import modelformset_factory

from usuarios.models import Usuario
from .models import Protocolo, ProtocoloAnexo
from .forms import ProtocoloForm, ProtocoloPFForm, ProtocoloPJForm, ProtocoloAnexoForm


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
    provisional_number = gerar_numero_protocolo()
    
    if request.method == 'POST':
        form = ProtocoloForm(request.POST)
        if form.is_valid():
            protocolo = form.save(commit=False)
            protocolo.numero = provisional_number
            protocolo.usuario = request.user
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
def lancar_protocolo_pf(request):
    provisional_number = gerar_numero_protocolo()
    
    if request.method == 'POST':
        form = ProtocoloPFForm(request.POST)
        if form.is_valid():
            protocolo = form.save(commit=False)
            protocolo.numero = provisional_number
            protocolo.usuario = request.user
            protocolo.save()
            messages.success(request, f"Protocolo {protocolo.numero} salvo com sucesso.")
            return redirect('protocolos:comprovante', protocolo_id=protocolo.id)
    else:
        form = ProtocoloPFForm()
    
    return render(request, 'protocolos/lancar_protocolo_pf.html', {
        'form': form,
        'protocolo_numero': provisional_number,
    })

@login_required
def lancar_protocolo_pj(request):
    provisional_number = gerar_numero_protocolo()
    data_hora = timezone.localtime(timezone.now()).strftime('%d/%m/%Y %H:%M:%S')
    
    AnexoFormSet = modelformset_factory(ProtocoloAnexo, form=ProtocoloAnexoForm, extra=15, max_num=15)
    
    if request.method == 'POST':
        form = ProtocoloPJForm(request.POST, request.FILES)
        formset = AnexoFormSet(request.POST, request.FILES, queryset=ProtocoloAnexo.objects.none())

        if form.is_valid() and formset.is_valid():
            protocolo = form.save(commit=False)
            protocolo.numero = provisional_number
            protocolo.data_hora_lancamento = timezone.now()
            protocolo.status = 'pendente'
            protocolo.usuario = request.user
            protocolo.save()
            for form in formset:
                if form.cleaned_data:
                    anexo = form.save(commit=False)
                    anexo.protocolo = protocolo
                    anexo.save()
            messages.success(request, f"Protocolo {protocolo.numero} salvo com sucesso.")
            return redirect('protocolos:comprovante', protocolo_id=protocolo.id)
        else:
            messages.error(request, "Erro ao salvar o protocolo. Verifique os dados e tente novamente.")
    else:
        form = ProtocoloPJForm()
        formset = AnexoFormSet(queryset=ProtocoloAnexo.objects.none())

    return render(request, 'protocolos/lancar_protocolo_pj.html', {
        'form': form,
        'formset': formset,
        'protocolo_numero': provisional_number,
        'data_hora': data_hora,
    })

@login_required
def visualizar_protocolo(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    return render(request, 'protocolos/visualizar_protocolo.html', {'protocolo': protocolo})

@login_required
def pesquisa_protocolos(request):
    query = request.GET.get('q', '')
    if query:
        protocolos = Protocolo.objects.filter(
            Q(numero__icontains=query) | Q(descricao__icontains=query)
        )
    else:
        protocolos = Protocolo.objects.all()

    paginator = Paginator(protocolos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'protocolos/pesquisa_protocolos.html', {
        'protocolos_paginados': page_obj,
        'query': query,
    })

@login_required
def editar_protocolo(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
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
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
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

def criar_protocolo(request):
    if request.method == 'POST':
        form = ProtocoloForm(request.POST)
        anexo_formset = modelformset_factory(ProtocoloAnexo, form=ProtocoloAnexoForm, extra=15, max_num=15)
        formset = anexo_formset(request.POST, request.FILES, queryset=ProtocoloAnexo.objects.none())

        if form.is_valid() and formset.is_valid():
            protocolo = form.save()
            for form in formset.cleaned_data:
                if form:
                    anexo = form['arquivo']
                    ProtocoloAnexo.objects.create(protocolo=protocolo, arquivo=anexo)
            return redirect('protocolo_sucesso')
    else:
        form = ProtocoloForm()
        anexo_formset = modelformset_factory(ProtocoloAnexo, form=ProtocoloAnexoForm, extra=15, max_num=15)
        formset = anexo_formset(queryset=ProtocoloAnexo.objects.none())

    return render(request, 'protocolos/criar_protocolo.html', {'form': form, 'formset': formset})

def criar_protocolo_pj(request):
    if request.method == 'POST':
        form = ProtocoloPJForm(request.POST)
        anexo_formset = modelformset_factory(ProtocoloAnexo, form=ProtocoloAnexoForm, extra=15, max_num=15)
        formset = anexo_formset(request.POST, request.FILES, queryset=ProtocoloAnexo.objects.none())

        if form.is_valid() and formset.is_valid():
            protocolo = form.save()
            for form in formset.cleaned_data:
                if form:
                    anexo = form['arquivo']
                    ProtocoloAnexo.objects.create(protocolo=protocolo, arquivo=anexo)
            return redirect('protocolo_sucesso')
    else:
        form = ProtocoloPJForm()
        anexo_formset = modelformset_factory(ProtocoloAnexo, form=ProtocoloAnexoForm, extra=15, max_num=15)
        formset = anexo_formset(queryset=ProtocoloAnexo.objects.none())

    return render(request, 'protocolos/lancar_protocolo_pj.html', {'form': form, 'formset': formset})
