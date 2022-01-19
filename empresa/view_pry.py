from django.core.checks import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from empresa.models import Proyecto
from .forms import ProyectoModelForm
from django.contrib import messages

def mostrar_pry(request):
    listProyectos = Proyecto.objects.all()
    context = { 'proyecto': listProyectos }
    return render(request,'empresa/proyectos.html',context)