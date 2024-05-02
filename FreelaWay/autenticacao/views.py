from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth

def cadastro(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/jobs/encontrar_jobs')
        return render(request, 'cadastro.html')
    
    if request.method == "POST":
        nome = request.POST.get('username')
        senha = request.POST.get('password')
        confirm_senha = request.POST.get('confirm-password')

        if len(nome.strip()) == 0 or len(senha.strip()) == 0:
            messages.add_message(request,constants.ERROR,'Preencha os campos em branco.')
            return redirect('/auth/cadastro')
        
        if not senha == confirm_senha:
            messages.add_message(request,constants.ERROR,'As senhas não coincidem.')
            return redirect('/auth/cadastro')
        
        if len(senha.strip()) <= 6:
            messages.add_message(request,constants.ERROR,'Senha inválida, digite no minímo 6 caracteres.')
            return redirect('/auth/cadastro')
        
        user = User.objects.filter(username = nome)
        if user.exists():
            messages.add_message(request,constants.ERROR,'Usuário já cadastrado, tente realizar o Login.')
            return redirect('/auth/cadastro')
        
        
        try:
            usuario = User.objects.create_user(username=nome, password=senha)
            usuario.save()
            messages.add_message(request,constants.SUCCESS,'Cadastro realizado com sucesso!')
            return redirect('/auth/login/')
        
        except:
            messages.add_message(request,constants.ERROR,'Erro interno do sistema.')
            return redirect('/auth/cadastro')
        
        



def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/jobs/encontrar_jobs')
        return render(request,'login.html')
    
    if request.method == "POST":
        nome = request.POST.get('username')
        senha = request.POST.get('password')
        
        usuario = auth.authenticate(request,username= nome, password = senha)

        if usuario:
            auth.login(request,usuario)
            return redirect('/jobs/encontrar_jobs')

        if not usuario:
            messages.add_message(request,constants.ERROR,'Credenciais inválidas.')
            return redirect('/auth/login/')
        
        
        

def sair(request):
    auth.logout(request)
    return redirect('/auth/login/')