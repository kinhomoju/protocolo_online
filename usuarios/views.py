from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Usuario, Perfil
from .forms import UsuarioCadastroForm, PerfilPJForm, PerfilPFForm
from django import forms

# Formulário de login (caso não tenha um UsuarioLoginForm no arquivo forms.py)
class UsuarioLoginForm(forms.Form):
    username = forms.CharField(label="Usuário", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# Cadastro de usuários
def cadastro(request):
    if request.method == 'POST':
        form = UsuarioCadastroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            return redirect('usuarios:login')
    else:
        form = UsuarioCadastroForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})

# Login de usuários
def login_usuario(request):
    if request.method == 'POST':
        form = UsuarioLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if not user.is_approved:
                    messages.warning(request, "Seu cadastro ainda não foi aprovado. Aguarde a aprovação de um administrador.")
                    return redirect('usuarios:nao_aprovado')
                
                login(request, user)
                # Se o usuário ainda não tem perfil completo, redirecione para a view de completar cadastro
                if not hasattr(user, 'perfil'):
                    return redirect('usuarios:completar_cadastro')
                if user.is_master:
                    return redirect('usuarios:dashboard_master')
                else:
                    return redirect('usuarios:dashboard')
            else:
                form.add_error(None, "Credenciais inválidas")
    else:
        form = UsuarioLoginForm()

    return render(request, 'usuarios/login.html', {'form': form})

# View para completar o cadastro (primeiro acesso do usuário comum aprovado)
@login_required
def completar_cadastro(request):
    # Se o usuário já possui um perfil, redirecione para o dashboard
    if hasattr(request.user, 'perfil'):
        if request.user.is_master:
            return redirect('usuarios:dashboard_master')
        return redirect('usuarios:dashboard')
    
    # O usuário aprovado deve ter seu campo 'tipo' preenchido pelo master
    tipo = request.user.tipo  # Espera 'PJ' ou 'PF'
    if not tipo:
        messages.error(request, "O seu tipo de cadastro não foi definido. Por favor, contate o administrador.")
        return redirect('usuarios:dashboard')
    
    if request.method == 'POST':
        if tipo == 'PJ':
            form = PerfilPJForm(request.POST)
        else:
            form = PerfilPFForm(request.POST)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.usuario = request.user
            perfil.save()
            messages.success(request, "Cadastro complementar realizado com sucesso.")
            if request.user.is_master:
                return redirect('usuarios:dashboard_master')
            else:
                return redirect('usuarios:dashboard')
    else:
        if tipo == 'PJ':
            form = PerfilPJForm()
        else:
            form = PerfilPFForm()
    return render(request, 'usuarios/completar_cadastro.html', {'form': form})

# Dashboard para usuários comum
@login_required
def dashboard(request):
    if not request.user.is_approved:
        return render(request, 'usuarios/nao_aprovado.html')
    
    # Verifica se o usuário possui perfil; caso contrário, redirecione para completar cadastro
    if not hasattr(request.user, 'perfil'):
        return redirect('usuarios:completar_cadastro')
    
    # Supondo que você tenha implementado uma forma de filtrar os protocolos lançados pelo usuário
    from protocolos.models import Protocolo  # Importação local para evitar dependência circular
    protocolos_usuario = Protocolo.objects.filter(usuario=request.user).order_by('-data_criacao')
    
    return render(request, 'usuarios/dashboard.html', {
        'protocolos_usuario': protocolos_usuario,
    })

# Dashboard para usuários master
@login_required
def dashboard_master(request):
    if not request.user.is_approved:
        return render(request, 'usuarios/nao_aprovado.html')
    
    if request.user.is_master:
        cadastros_pendentes = Usuario.objects.filter(is_approved=False).count()
        return render(request, 'usuarios/dashboard_master.html', {'cadastros_pendentes': cadastros_pendentes})
    
    return redirect('usuarios:dashboard')

# Aprovação de usuários pendentes
@login_required
def aprovar_usuarios(request):
    if request.user.is_authenticated and hasattr(request.user, 'is_master') and request.user.is_master:
        usuarios_pendentes = Usuario.objects.filter(is_approved=False)
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            approval_status = request.POST.get('approval_status')  # 'aprovar' ou 'rejeitar'
            usuario = get_object_or_404(Usuario, id=user_id)
            
            if approval_status == 'aprovar':
                cadastro_origem = request.POST.get('cadastro_origem')  # Deve ser 'PJ' ou 'PF'
                if cadastro_origem not in ['PJ', 'PF']:
                    messages.error(request, "Selecione uma opção válida para a origem do cadastro.")
                    return redirect('usuarios:aprovar_usuarios')
                
                if cadastro_origem == 'PJ':
                    # Se for externo (PJ), define automaticamente como usuário normal
                    usuario.tipo = 'PJ'
                    usuario.is_master = False
                else:  # cadastro_origem == 'PF' (interno)
                    usuario.tipo = 'PF'
                    nivel = request.POST.get('nivel')  # Deve ser 'M' ou 'N'
                    if nivel not in ['M', 'N']:
                        messages.error(request, "Selecione um nível válido para usuário interno.")
                        return redirect('usuarios:aprovar_usuarios')
                    usuario.is_master = True if nivel == 'M' else False
                usuario.is_approved = True
                usuario.save()
                if usuario.tipo == 'PJ':
                    tipo_text = "Usuário Externo (PJ) - Normal"
                else:
                    tipo_text = "Usuário Interno (PF) - " + ("Master" if usuario.is_master else "Normal")
                messages.success(request, f"Usuário {usuario.nome} aprovado como {tipo_text}.")
            elif approval_status == 'rejeitar':
                usuario.delete()
                messages.success(request, f"Usuário {usuario.nome} rejeitado e excluído com sucesso.")
            
            return redirect('usuarios:aprovar_usuarios')
        return render(request, 'usuarios/aprovar_usuarios.html', {'usuarios_pendentes': usuarios_pendentes})
    return redirect('usuarios:login')

# Exclusão de usuários aprovados (apenas para master)
@login_required
def excluir_usuarios(request, user_id=None):
    """
    Lista os usuários aprovados para exclusão com paginação.
    Apenas usuários master podem acessar essa funcionalidade.
    """
    if request.user.is_authenticated and request.user.is_master:
        usuarios = Usuario.objects.filter(is_approved=True).order_by('-id')  # Ordena do mais recente para o mais antigo
        paginator = Paginator(usuarios, 10)  # Exibir 10 usuários por página

        page_number = request.GET.get('page')
        usuarios_paginados = paginator.get_page(page_number)

        return render(request, 'usuarios/excluir_usuarios.html', {'usuarios_paginados': usuarios_paginados})
    
    return redirect('usuarios:login')

@login_required
def excluir_usuario(request, user_id):
    """
    Exclui um usuário específico se o usuário logado for um master.
    """
    if request.user.is_authenticated and request.user.is_master:
        usuario = get_object_or_404(Usuario, id=user_id)
        usuario.delete()
        messages.success(request, f'Usuário {usuario.nome} foi excluído com sucesso.')
        return redirect('usuarios:excluir_usuarios')
    
    return redirect('usuarios:login')

# Pesquisa de usuários para o dashboard master
@login_required
def pesquisa_usuarios(request):
    query = request.GET.get('q', '')
    usuarios_pesquisa = None
    if query:
        usuarios_pesquisa = Usuario.objects.filter(
            nome__icontains=query
        ) | Usuario.objects.filter(
            username__icontains=query
        ) | Usuario.objects.filter(
            email__icontains=query
        )
    cadastros_pendentes = Usuario.objects.filter(is_approved=False).count()
    return render(request, 'usuarios/dashboard_master.html', {
        'usuarios_pesquisa': usuarios_pesquisa,
        'cadastros_pendentes': cadastros_pendentes,
    })

# Logout de usuários
@login_required
def logout_usuario(request):
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('usuarios:login')

def nao_aprovado(request):
    return render(request, 'usuarios/nao_aprovado.html')
