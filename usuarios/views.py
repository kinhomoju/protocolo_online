import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator

from protocolos.models import Protocolo
from .models import Usuario, Perfil
from .forms import UsuarioCadastroForm, UsuarioLoginForm, PerfilPJForm, PerfilPFForm

# Configurar o logger
logger = logging.getLogger(__name__)

# Cadastro de usuários
def cadastro(request):
    if request.method == 'POST':
        form = UsuarioCadastroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_approved = False  # Cadastro precisa ser aprovado
            usuario.save()
            messages.success(request, 'Cadastro realizado! Aguarde a aprovação do administrador.')
            return redirect('usuarios:login')
    else:
        form = UsuarioCadastroForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})

# Login de usuários
def login_usuario(request):
    logger.debug("Iniciando o processo de login")
    if request.method == 'POST':
        logger.debug("Método POST recebido")
        form = UsuarioLoginForm(request.POST)
        if form.is_valid():
            logger.debug("Formulário de login é válido")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            logger.debug(f"Autenticando usuário: {username}")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                logger.debug(f"Usuário autenticado: {user.username}")
                if not user.is_approved:
                    logger.warning(f"Usuário não aprovado: {user.username}")
                    messages.warning(request, "Seu cadastro ainda não foi aprovado. Aguarde a aprovação de um administrador.")
                    return redirect('usuarios:nao_aprovado')

                login(request, user)
                logger.debug(f"Usuário logado: {user.username}")
                if not hasattr(user, 'perfil'):
                    return redirect('usuarios:completar_cadastro')
                elif user.is_master:
                    return redirect('usuarios:dashboard_master')
                else:
                    return redirect('usuarios:dashboard')
            else:
                logger.error("Credenciais inválidas")
                form.add_error(None, "Credenciais inválidas")
                messages.error(request, "Credenciais inválidas")
        else:
            logger.error("Formulário inválido")
            logger.error(form.errors)
            for field in form:
                logger.error(f"Erro no campo {field.name}: {field.errors}")
            messages.error(request, "Formulário inválido")
    else:
        logger.debug("Método GET recebido")
        form = UsuarioLoginForm()

    return render(request, 'usuarios/login.html', {'form': form})

# View para completar o cadastro
@login_required
def completar_cadastro(request):
    if hasattr(request.user, 'perfil'):
        if request.user.is_master:
            return redirect('usuarios:dashboard_master')
        return redirect('usuarios:dashboard')

    tipo = request.user.tipo
    if not tipo:
        messages.error(request, "Seu tipo de cadastro não foi definido. Contate o administrador.")
        return redirect('usuarios:dashboard')

    form_class = PerfilPJForm if tipo == 'PJ' else PerfilPFForm

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.usuario = request.user
            perfil.save()
            messages.success(request, "Cadastro complementar concluído com sucesso.")
            if request.user.is_master:
                return redirect('usuarios:dashboard_master')
            else:
                return redirect('usuarios:dashboard')
    else:
        form = form_class()

    return render(request, 'usuarios/completar_cadastro.html', {'form': form})

# Dashboard para usuários comuns
@login_required
def dashboard(request):
    if not request.user.is_approved:
        return render(request, 'usuarios/nao_aprovado.html')
    
    # Verifica se o usuário possui perfil; caso contrário, redirecione para completar cadastro
    if not hasattr(request.user, 'perfil'):
        return redirect('usuarios:completar_cadastro')
    
    from protocolos.models import Protocolo
    protocolos_usuario = Protocolo.objects.filter(usuario=request.user).order_by('-data_criacao')

    return render(request, 'usuarios/dashboard.html', {'protocolos_usuario': protocolos_usuario})

# Dashboard para usuários master
@login_required
def dashboard_master(request):
    if not request.user.is_approved:
        return render(request, 'usuarios/nao_aprovado.html')

    if request.user.is_master:
        cadastros_pendentes = Usuario.objects.filter(is_approved=False).count()
        ultimos_usuarios = Usuario.objects.filter(is_approved=True).order_by('-id')[:10]
        ultimos_protocolos = Protocolo.objects.all().order_by('-data_criacao')[:10]

        return render(request, 'usuarios/dashboard_master.html', {
            'cadastros_pendentes': cadastros_pendentes,
            'ultimos_usuarios': ultimos_usuarios,
            'ultimos_protocolos': ultimos_protocolos,
        })

    return redirect('usuarios:dashboard')

# Aprovação de usuários pendentes
@login_required
def aprovar_usuarios(request):
    if not request.user.is_master:
        return redirect('usuarios:dashboard')

    usuarios_pendentes = Usuario.objects.filter(is_approved=False)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        usuario = get_object_or_404(Usuario, id=user_id)
        approval_status = request.POST.get('approval_status')

        if approval_status == 'aprovar':
            cadastro_origem = request.POST.get('cadastro_origem')
            if cadastro_origem not in ['PJ', 'SP']:
                messages.error(request, "Selecione um tipo válido para o usuário.")
                return redirect('usuarios:aprovar_usuarios')

            usuario.tipo = cadastro_origem
            usuario.is_master = request.POST.get('nivel') == 'M' if cadastro_origem == 'SP' else False
            usuario.is_approved = True
            usuario.save()

            messages.success(request, f"Usuário {usuario.nome} aprovado como {usuario.tipo}.")
        elif approval_status == 'rejeitar':
            usuario.delete()
            messages.success(request, f"Usuário {usuario.nome} foi excluído.")

        return redirect('usuarios:aprovar_usuarios')

    return render(request, 'usuarios/aprovar_usuarios.html', {'usuarios_pendentes': usuarios_pendentes})

# Exclusão de usuários aprovados (apenas para master)
@login_required
def excluir_usuarios(request):
    if not request.user.is_master:
        return redirect('usuarios:dashboard')

    usuarios = Usuario.objects.filter(is_approved=True).order_by('-id')
    paginator = Paginator(usuarios, 10)
    page_number = request.GET.get('page')
    usuarios_paginados = paginator.get_page(page_number)

    return render(request, 'usuarios/excluir_usuarios.html', {'usuarios_paginados': usuarios_paginados})

@login_required
def excluir_usuario(request, user_id):
    if not request.user.is_master:
        return redirect('usuarios:dashboard')

    usuario = get_object_or_404(Usuario, id=user_id)
    usuario.delete()
    messages.success(request, f'Usuário {usuario.nome} foi excluído com sucesso.')

    return redirect('usuarios:excluir_usuarios')

# Pesquisa de usuários para o dashboard master
@login_required
def pesquisa_usuarios(request):
    if not request.user.is_master:
        return redirect('usuarios:dashboard')

    query = request.GET.get('q')
    usuarios = Usuario.objects.filter(nome__icontains=query) if query else Usuario.objects.all()
    paginator = Paginator(usuarios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'usuarios/dashboard_master.html', {'usuarios_pesquisa': page_obj})

# Logout de usuários
@login_required
def logout_usuario(request):
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('usuarios:login')

def nao_aprovado(request):
    return render(request, 'usuarios/nao_aprovado.html')
