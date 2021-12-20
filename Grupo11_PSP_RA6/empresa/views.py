from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

#---------Enlace a la plantilla escogida para el proyecto--------#
class InicioEmpresaView(TemplateView):
    template_name = "empresa/page_inicio.html"