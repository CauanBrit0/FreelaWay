from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from .models import Jobs,Referencias
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required(login_url="/auth/login")
def encontrar_jobs(request):     
    if request.method == "GET":         
        preco_minimo = request.GET.get('preco_minimo')         
        preco_maximo = request.GET.get('preco_maximo')          
        prazo_minimo = request.GET.get('prazo_minimo')         
        prazo_maximo = request.GET.get('prazo_maximo')          
        categoria = request.GET.get('categoria')          
        if preco_minimo or preco_maximo or prazo_minimo or prazo_maximo or categoria:             
            if not preco_minimo:                 
                preco_minimo = 0              
            if not preco_maximo:                 
                preco_maximo = 999999              
                if not prazo_minimo:                 
                    prazo_minimo = datetime(year=1900, month=1, day=1)
            if not prazo_maximo:                 
                prazo_maximo = datetime(year=3000, month=1, day=1)

            if categoria =='D':
                categoria = ['D',]

            if categoria =='EV':
                categoria = ['EV',]                         
            
            jobs = Jobs.objects.filter(preco__gte=preco_minimo)\
                .filter(preco__lte=preco_maximo)\
                .filter(prazo_entrega__gte=prazo_minimo)\
                .filter(prazo_entrega__lte=prazo_maximo)\
                .filter(categoria__in=categoria)      
        else:             
            jobs = Jobs.objects.filter(reservado=False)          
        return render(request, 'encontrar_jobs.html', {'jobs': jobs})
    

@login_required(login_url="/auth/login")
def aceitar_job(request, id):
    jobs = Jobs.objects.get(id = id)
    jobs.profissional = request.user
    jobs.reservado = True
    jobs.save()
    return redirect('/jobs/encontrar_jobs/')


@login_required(login_url="/auth/login")
def perfil(request):
    if request.method =="GET":
        jobs = Jobs.objects.filter(profissional_id = request.user)
        return render(request, 'perfil.html',{'jobs':jobs})
    
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')

        usuario = User.objects.filter(username=username).exclude(id=request.user.id)
        if usuario.exists():
            messages.add_message(request,constants.ERROR,'Nome de Usuário já utilizado, tente outro.')
            return redirect('/jobs/perfil/')
        
        usuario = User.objects.filter(email=email).exclude(id=request.user.id)

        if User.objects.filter(email = email):
            messages.add_message(request,constants.ERROR,'Email já utilizado, tente outro.')
            return redirect('/jobs/perfil/')
        
        try:
            request.user.username = username
            request.user.email = email
            request.user.first_name = primeiro_nome
            request.user.last_name = ultimo_nome
            request.user.save()
            messages.add_message(request,constants.SUCCESS,'Informações atualizadas com sucesso.')
            return redirect('/jobs/perfil/')
        
        except:
            messages.add_message(request,constants.ERROR,'Erro interno do sistema')
            return redirect('/jobs/perfil/')



@login_required(login_url="/auth/login")
def enviar_projeto(request):
    arquivo = request.FILES.get('file')
    id_job = request.POST.get('id')

    jobs = Jobs.objects.get(id = id_job)
    jobs.arquivo_final = arquivo
    jobs.status = "AA"
    jobs.save()
    return redirect('/jobs/perfil/')