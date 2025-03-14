import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from django.forms import modelformset_factory

from usuarios.models import Usuario
from .models import ProtocoloPF, ProtocoloPJ, ProtocoloAnexo
from .forms import ProtocoloPFForm, ProtocoloPJForm, ProtocoloAnexoForm


def gerar_numero_protocolo(modelo):
    now = timezone.localtime(timezone.now())
    date_prefix = now.strftime('%d%m%Y')
    time_part = now.strftime('%H%M%S')
    
    count = modelo.objects.filter(numero__startswith=date_prefix).count() + 1
    sequence = str(count).zfill(4)
    
    return date_prefix + time_part + sequence


@login_required
def lancar_protocolo_pf(request):
    provisional_number = gerar_numero_protocolo(ProtocoloPF)
    
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


def obter_data_hora():
    return timezone.localtime(timezone.now()).strftime('%d/%m/%Y %H:%M:%S')


AnexoFormset = modelformset_factory(ProtocoloAnexo, form=ProtocoloAnexoForm, extra=15, max_num=15)

# Configurar o logger
logger = logging.getLogger(__name__)


@login_required
def lancar_protocolo_pj(request):
    provisional_number = gerar_numero_protocolo(ProtocoloPJ)
    data_hora = obter_data_hora()
    
    if request.method == 'POST':
        logger.info("Recebido POST request para salvar protocolo PJ.")
        form = ProtocoloPJForm(request.POST, request.FILES)
        formset = AnexoFormset(request.POST, request.FILES, queryset=ProtocoloAnexo.objects.none())

        if form.is_valid() and formset.is_valid():
            logger.info("Formulário e formset são válidos.")
            protocolo = form.save(commit=False)
            protocolo.numero = provisional_number
            protocolo.data_hora_lancamento = timezone.now()
            protocolo.status = 'pendente'
            protocolo.usuario = request.user
            protocolo.save()

            for form_data in formset.cleaned_data:
                if form_data:
                    ProtocoloAnexo.objects.create(protocolo=protocolo, arquivo=form_data['arquivo'])

            messages.success(request, f"Protocolo {protocolo.numero} salvo com sucesso.")
            logger.info(f"Protocolo {protocolo.numero} salvo com sucesso.")
            return redirect('protocolos:comprovante', protocolo_id=protocolo.id)
        else:
            logger.error("Erro ao salvar o protocolo. Verifique os dados e tente novamente.")
            logger.error(f"Erros no formulário: {form.errors}")
            logger.error(f"Erros no formset: {formset.errors}")
            messages.error(request, "Erro ao salvar o protocolo. Verifique os dados e tente novamente.")
    else:
        form = ProtocoloPJForm()
        formset = AnexoFormset(queryset=ProtocoloAnexo.objects.none())

    return render(request, 'protocolos/lancar_protocolo_pj.html', {
        'form': form,
        'formset': formset,
        'protocolo_numero': provisional_number,
        'data_hora': data_hora,
    })


@login_required
def visualizar_protocolo(request, protocolo_id):
    protocolo = get_object_or_404(ProtocoloPF, id=protocolo_id) or get_object_or_404(ProtocoloPJ, id=protocolo_id)
    return render(request, 'protocolos/visualizar_protocolo.html', {'protocolo': protocolo})


@login_required
def pesquisa_protocolos(request):
    query = request.GET.get('q', '').strip()

    protocolos_pf = ProtocoloPF.objects.select_related('usuario').only('id', 'numero', 'descricao', 'usuario_id')
    protocolos_pj = ProtocoloPJ.objects.select_related('usuario').only('id', 'numero', 'descricao', 'usuario_id')

    protocolos = protocolos_pf.union(protocolos_pj).order_by('-data_hora_lancamento')

    if query:
        protocolos = protocolos.filter(Q(numero__icontains=query) | Q(descricao__icontains=query))

    paginator = Paginator(protocolos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'protocolos/pesquisa_protocolos.html', {
        'protocolos_paginados': page_obj,
        'query': query,
    })


@login_required
def excluir_protocolo(request, protocolo_id):
    protocolo = None

    if ProtocoloPF.objects.filter(id=protocolo_id).exists():
        protocolo = get_object_or_404(ProtocoloPF, id=protocolo_id)
    elif ProtocoloPJ.objects.filter(id=protocolo_id).exists():
        protocolo = get_object_or_404(ProtocoloPJ, id=protocolo_id)

    if not protocolo:
        messages.error(request, "Protocolo não encontrado.")
        return redirect('protocolos:pesquisa_protocolos')

    if protocolo.status in {'pago', 'rejeitado', 'devolvido'}:
        messages.error(request, "Este protocolo não pode ser excluído.")
        return redirect('protocolos:pesquisa_protocolos')

    if request.method == 'POST':
        protocolo.delete()
        messages.success(request, "Protocolo excluído com sucesso.")
        return redirect('protocolos:pesquisa_protocolos')

    return render(request, 'protocolos/confirmar_exclusao.html', {'protocolo': protocolo})


@login_required
def comprovante_protocolo(request, protocolo_id):
    protocolo = None

    if ProtocoloPF.objects.filter(id=protocolo_id).exists():
        protocolo = get_object_or_404(ProtocoloPF, id=protocolo_id)
    elif ProtocoloPJ.objects.filter(id=protocolo_id).exists():
        protocolo = get_object_or_404(ProtocoloPJ, id=protocolo_id)

    if not protocolo:
        messages.error(request, "Protocolo não encontrado.")
        return redirect('protocolos:pesquisa_protocolos')

    return render(request, 'protocolos/comprovante_protocolo.html', {'protocolo': protocolo})


@login_required
def editar_protocolo(request, protocolo_id):
    protocolo_pf = ProtocoloPF.objects.filter(id=protocolo_id).first()
    protocolo_pj = ProtocoloPJ.objects.filter(id=protocolo_id).first()

    if protocolo_pf:
        form_class = ProtocoloPFForm
        protocolo = protocolo_pf
    elif protocolo_pj:
        form_class = ProtocoloPJForm
        protocolo = protocolo_pj
    else:
        messages.error(request, "Protocolo não encontrado.")
        return redirect('protocolos:pesquisa_protocolos')

    if request.method == 'POST':
        form = form_class(request.POST, instance=protocolo)
        formset = AnexoFormset(request.POST, request.FILES, queryset=protocolo.anexos.all())

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f"Protocolo {protocolo.numero} atualizado com sucesso.")
            return redirect('protocolos:visualizar_protocolo', protocolo_id=protocolo.id)
        else:
            messages.error(request, "Erro ao atualizar o protocolo. Verifique os dados e tente novamente.")
    else:
        form = form_class(instance=protocolo)
        formset = AnexoFormset(queryset=protocolo.anexos.all())

    return render(request, 'protocolos/editar_protocolo.html', {
        'form': form,
        'formset': formset,
        'protocolo': protocolo,
    })
