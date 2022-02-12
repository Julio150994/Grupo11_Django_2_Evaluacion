from datetime import datetime
from django.core.checks import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from empresa.models import Categoria, Cliente, Empleado, Participa, Proyecto, Usuario
from .forms import CategoriaModelForm, ClienteModelForm, ParticipaModelForm, UsuarioModelForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from django.views.generic import View



def mostrar_clientes_pry(request,id):
    proyecto = Proyecto.objects.get(id = id)
    print("Id proyecto: "+str(proyecto))
    
    hoy = datetime.now().strftime('%d/%M/%Y')
    
    #id_emp = Empleado.objects.get(id = empleado_id)
    
    listPryClientes = Participa.objects.order_by('-id').all() #primero visualizar los clientes en proyectos del empleado#
    context = {'proyecto':proyecto, 'participas':listPryClientes, 'date':hoy }
    
    return render(request,"empresa/ver_clientes_empleado.html",context)


def annadir_inscripcion_pry(request, cliente_id):
    id_cliente = Cliente.objects.get(id=cliente_id)
    
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    proyectos = Proyecto.objects.order_by('id').all()
    
    usuario = UsuarioModelForm()
    cliente = ClienteModelForm()
    categoria = CategoriaModelForm()
    participa = ParticipaModelForm()
    context = {
        'cliente':id_cliente,
        'proyectos':proyectos,
        'usuario':usuario,
        'cli':cliente,
        'categoria':categoria,
        'participa': participa
    }

    if request.POST:
        usuario = UsuarioModelForm(request.POST)
        cliente = ClienteModelForm(request.POST)
        categoria = CategoriaModelForm(request.POST,request.FILES)
        participa = ParticipaModelForm(request.POST)
        context = {
            'cliente':id_cliente,
            'proyectos':proyectos,
            'usuario':usuario,
            'cli':cliente,
            'categoria':categoria,
            'participa': participa
        }
        
        if participa.is_valid():
            idCliente = request.POST.get("idCliente",id_cliente)
            idProyecto = request.POST.get("idProyecto")
            fechaInscripcion = request.POST.get("fechaInscripcion")
            rol = request.POST.get("rol")
            
            # Realizamos la comprobación de fechas #
            if fechaInscripcion < fecha_actual:
                if idCliente is not None or idProyecto is not None or fechaInscripcion is not None or rol is not None:
                    participa_pry = Participa(idCliente=idCliente, idProyecto=Proyecto.objects.get(id=idProyecto), fechaInscripcion=fechaInscripcion, rol=rol)
                    participa_pry.save()
                    messages.success(request,'Se ha inscrito al proyecto correctamente.')
                    return redirect('proyectos')
            else:
                messages.error(request,'La fecha de inscripción no puede realizarse hoy, ni posteriormente.')
                return redirect('inscripcion_pry')    
        else:
            messages.warning(request,'Faltan datos por introducir.')
            return redirect('inscripcion_pry')

    return render(request, "empresa/inscripcion_pry.html",context)


def buscar_clientes_pry(request):
    nombre_rol = request.GET.get("search")
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    
    list_usuarios = Usuario.objects.all()
    list_empleados = Empleado.objects.all()
    list_proyectos = Proyecto.objects.all()
    list_clientes_emp = Participa.objects.all()
    
    context = {
        'usuarios':list_usuarios,
        'empleados':list_empleados,
        'proyectos':list_proyectos,
        'participas':list_clientes_emp,
        'fechaActual':fecha_actual
    }    

    if nombre_rol:
        #__icontains = para evitar errores de tipo case sensitive#
        resultado = Participa.objects.filter(Q(rol__icontains=nombre_rol))
        
        context = {
            'usuarios':list_usuarios,
            'empleados':list_empleados,
            'proyectos':list_proyectos,
            'participas':resultado,
            'fechaActual':fecha_actual
        }
    
    return render(request,"empresa/buscar_clientes.html",context)


class InformeClientePDFView(View):
    
    def header(self, cliente_pdf):
        logo_salesianos = settings.MEDIA_ROOT+'\logo_informe.png'
        cliente_pdf.drawImage(logo_salesianos, 20, 765, 40, 70, preserveAspectRatio=True)
        
        cliente_pdf.setFont("Helvetica-Bold", 25)
        cliente_pdf.setFillColorRGB(0.29296875, 0.453125, 0.609375)
        cliente_pdf.drawString(136, 790, u"INFORME PDF DE SALESEMP")
        
        cliente_pdf.setFont('Times-Roman',17)
        cliente_pdf.setFillColorRGB(0.21, 0.139, 0.37)
        cliente_pdf.drawString(10, 690, u"DATOS DE CLIENTE")
        
        cliente_pdf.setFont('Times-Roman',17)
        cliente_pdf.setFillColorRGB(0.21, 0.139, 0.37)
        cliente_pdf.drawString(10, 570, u"PROYECTOS DEL CLIENTE")
    
    def tabla_datos_cliente(self, cliente_pdf, posicion_y, cliente_id):
        campos = ("Dni","Nombre","Apellidos","Dirección","Fecha de Nacimiento","Fecha de Alta","Usuario")
        
        datos_cliente = [(cliente.dni, cliente.nombre, cliente.apellidos, cliente.direccion,
                    cliente.fechaNacimiento, cliente.fechaAlta, cliente.idUsuario.username) for cliente in cliente_id ]
        ver_tabla_cliente = Table([campos] + datos_cliente)
        
        # Aplicamos estilos para nuestras celdas #
        ver_tabla_cliente.setStyle(TableStyle(
            [
                #Campos de tabla cliente#
                ('ALIGN',(0,0),(3,0),'CENTER'),
                ('GRID',(0,0), (-1, -1), 1, colors.red),
                ('FONTSIZE',(0, 0),(-1, -1), 10),
            ]
        ))
        
        ver_tabla_cliente.wrapOn(cliente_pdf, 500, 350) # anchura y altura de la tabla#
        ver_tabla_cliente.drawOn(cliente_pdf, 10, posicion_y) # coordenada que se mostrará en la tabla#
        return ver_tabla_cliente
    
    def tabla_proyectos_cliente(self, cliente_pdf, posicion_y, cliente_id):
        campos = ("Titulo","Descripción","Nivel","Fecha de Inicio", "Fecha Fin", "Informe final")
        
        proyectos_cliente = [(proyecto.titulo, proyecto.descripcion, proyecto.nivel, proyecto.fechaInicio,
                    proyecto.fechaFin, proyecto.informeFinal) for proyecto in Proyecto.objects.order_by('-id').all()]
        ver_tabla_proyectos = Table([campos] + proyectos_cliente)
        
        ver_tabla_proyectos.setStyle(TableStyle(
            [
                ('ALIGN',(0,0),(3,0),'CENTER'),
                ('GRID',(0,0), (-2, -1), 1, colors.blue),
                ('FONTSIZE',(0, 0),(-1, -1), 10),
            ]
        ))
        
        ver_tabla_proyectos.wrapOn(cliente_pdf, 500, 350)
        ver_tabla_proyectos.drawOn(cliente_pdf, 10, posicion_y)
        return ver_tabla_proyectos
    
    
    def get(self, request, cliente_id, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="informe.pdf"' #nombre del archivo descargado    
        
        buffer = BytesIO()
        cliente_pdf = canvas.Canvas(buffer, pagesize=A4)
        
        self.header(cliente_pdf)
        
        id_cliente = Cliente.objects.filter(id=cliente_id)
        posicion_cliente_y = 640
        self.tabla_datos_cliente(cliente_pdf,posicion_cliente_y, id_cliente)
        
        posicion_proyectos_y = 340
        self.tabla_proyectos_cliente(cliente_pdf,posicion_proyectos_y, id_cliente)
        
        cliente_pdf.showPage()
        cliente_pdf.save()
        
        cliente_pdf = buffer.getvalue()
        buffer.close()
        response.write(cliente_pdf)
        return response