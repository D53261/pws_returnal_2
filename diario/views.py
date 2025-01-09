from django.shortcuts import redirect, render
from django.http import HttpResponse
from datetime import datetime, timedelta

from diario.models import Pessoa, Diario, Usuario

user_actived = None 

def home(request):
    global user_actived
    if user_actived is None:
        return redirect('login')
    
    textos = Diario.objects.filter(user=user_actived).order_by('create_at')[:3]
    pessoas = Pessoa.objects.filter(user=user_actived)
    nomes = [pessoa.nome for pessoa in pessoas]
    qtds = []
    for pessoa in pessoas:
        qtd = Diario.objects.filter(pessoas=pessoa, user=user_actived).count()
        qtds.append(qtd)

    usuarios = Usuario.objects.all()
    nomes_usuarios = [usuario.nome for usuario in usuarios]
    diarios = []
    for usuario in usuarios:
        diario = Diario.objects.filter(user=usuario).order_by('create_at').count()
        diarios.append(diario)


    return render(request, 'home.html', {'textos': textos, 'nomes' : nomes, 'qtds': qtds, 'nomes_usuarios': nomes_usuarios, 'diarios': diarios})



def escrever(request):
    global user_actived
    if user_actived is None:
        return redirect('login')
    
    if request.method == 'GET':
        pessoas = Pessoa.objects.filter(user=user_actived)
        return render(request, 'escrever.html', {'pessoas': pessoas})
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        tags = request.POST.getlist('tags')
        pessoas = request.POST.getlist('pessoas')
        texto = request.POST.get('texto')
        funcional = ""

        if len(titulo.strip()) == 0 or len(texto.strip()) == 0:
            funcional = "Por favor, Preencha todos os campos"
            pessoas = Pessoa.objects.filter(user=user_actived)
            return render(request, 'escrever.html', {'funcional': funcional, 'pessoas': pessoas})

        diario = Diario(
            titulo=titulo,
            texto=texto,
            user=user_actived
        )
        diario.set_tags(tags)
        diario.save()

        for i in pessoas:
            pessoa = Pessoa.objects.get(id=i, user=user_actived)
            diario.pessoas.add(pessoa)

        diario.save()
        if pessoas != 0:
            funcional = "Diário cadastrado com sucesso"
            pessoas = Pessoa.objects.filter(user=user_actived)
            return render(request, 'escrever.html', {'funcional': funcional, 'pessoas': pessoas})

        return redirect('escrever')
    
def cadastrar_pessoa(request):
    global user_actived
    if user_actived is None:
        return redirect('login')
    
    if request.method == 'GET':
        return render(request, 'pessoa.html')
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        foto = request.FILES.get('foto')
        
        pessoa = Pessoa(
            nome=nome,
            foto=foto,
            user=user_actived
        )
        pessoa.save()
        return redirect('escrever')
    
def dia(request):
    global user_actived
    if user_actived is None:
        return redirect('login')
    
    data = request.GET.get('data')
    data_formatada = datetime.strptime(data, '%Y-%m-%d')
    diarios = Diario.objects.filter(create_at__gte=data_formatada, user=user_actived).filter(create_at__lte=data_formatada+timedelta(days=1), user=user_actived)
    # gte: maior ou igual a data informada; lte: menor ou igual a data informada
    return render(request, 'dia.html', {'diarios': diarios, 'total': diarios.count(), 'data': data})

def excluir_dia(request):
    global user_actived
    if user_actived is None:
        return redirect('login')
    
    dia = datetime.strptime(request.GET.get('data'), '%Y-%m-%d')
    diarios = Diario.objects.filter(create_at__gte=dia, user=user_actived).filter(create_at__lte=dia+timedelta(days=1), user=user_actived)
    diarios.delete()
    return redirect('home')

def registro(request):
    if request.method == 'GET':
        return render(request, 'registro.html')
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        funcional = ''

        if Usuario.objects.filter(nome=nome).exists():
            funcional = "Usuário já cadastrado"
            return render(request, 'registro.html', {'funcional': funcional})
        elif senha != confirmar_senha:
            funcional = "As senhas não conferem"
            return render(request, 'registro.html', {'funcional': funcional})
        
        usuario = Usuario(
            nome=nome,
            senha=senha
        )

        usuario.save()
        return redirect('login')
    
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        funcional = ''

        try:
            usuario = Usuario.objects.get(nome=nome, senha=senha)
            global user_actived
            user_actived = usuario
            return redirect('home')
        except Usuario.DoesNotExist:
            funcional = "Usuário ou senha inválidos"
            return render(request, 'login.html', {'funcional': funcional})