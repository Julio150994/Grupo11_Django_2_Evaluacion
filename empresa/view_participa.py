from datetime import datetime
import datetime
from tkinter.ttk import Style
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
from reportlab.platypus import Table, TableStyle, Paragraph, Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
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

def form_fechas(request, cliente_id):
    id_cliente = Cliente.objects.get(id=cliente_id)
    participas = Participa.objects.order_by('-idProyecto')
    participa = ParticipaModelForm()

    context = {
        'cliente':id_cliente,
        'participas':participas,
        'participa': participa
    }

    if request.GET:
         participa = ParticipaModelForm(request.GET)
         context = {
            'cliente':id_cliente,
            'participa':participa
         }

         if participa.is_valid():
            idCliente = request.GET.get("idCliente",id_cliente)
            idProyecto = request.GET.get("idProyecto")
            
            if idCliente is not None or idProyecto is not None:
                participa_pry = Participa(idCliente=idCliente, fechaInicio=Proyecto.objects.get(idProyecto), fechaFin=Proyecto.objects.get(idProyecto))
                return redirect('pdf')

    return render(request,"empresa/form_fechas.html", context)

class InformeClientePDFView(View):
    
    global style
    style = getSampleStyleSheet()['Normal']
    
    def header(self, cliente_pdf):
        logo_salesianos = settings.MEDIA_ROOT+'\logo_informe.png'
        cliente_pdf.drawImage(logo_salesianos, 10, 770, 40, 70, preserveAspectRatio=True)
        
        cliente_pdf.setFont("Helvetica-Bold", 25)
        cliente_pdf.setFillColorRGB(0.29296875, 0.453125, 0.609375)
        cliente_pdf.drawString(150, 795, u"INFORME PDF DE SALESEMP")
        
        cliente_pdf.setFont('Times-Roman',17)
        cliente_pdf.setFillColorRGB(0.21, 0.139, 0.37)
        cliente_pdf.drawString(10, 726, u"DATOS DE CLIENTE")
        
        cliente_pdf.setFont('Times-Roman',17)
        cliente_pdf.setFillColorRGB(0.21, 0.139, 0.37)
        cliente_pdf.drawString(10, 560, u"PROYECTOS DONDE PARTICIPA EL CLIENTE")
    
    def tabla_datos_cliente(self, cliente_pdf, posicion_y, cliente_id):
        encabezados = ('Dni','Nombre','Apellidos','Direccion')
        datos = [(c.dni, c.nombre, c.apellidos, c.direccion) for c in cliente_id]
        datos_orden = Table([encabezados] + datos, colWidths=[4*cm,4*cm,4*cm])
        datos_orden.setStyle(TableStyle(
            [
                ('ALIGN',(0,0),(3,4),'CENTER'),
                ('GRID', (0,0),(-1,-1),1,colors.transparent),
                ('FONTSIZE', (0,0),(-1,-1),10),
                 ('BACKGROUND',(0,0),(-1,-1),colors.Color(red=(250/255),green=(128/255),blue=(114/255), alpha=(125/255))),
                ('COLBACKGROUNDS',(0,1),(-1,-1),(colors.beige,colors.lightyellow)),
            ]
        ))
    
        datos_orden.wrapOn(cliente_pdf,800,600)
        datos_orden.drawOn(cliente_pdf,10,posicion_y)
        return datos_orden
    
    def Para(self,txt):
        return Paragraph(txt, style)

    def tabla_proyectos_cliente(self, cliente_pdf, posicion_y, usuario_cliente):
        encabezados = ('Titulo','Descripcion','Inicio','Fin','Foto de Categoría')
        datos = [(self.Para(p.idProyecto.titulo), self.Para(p.idProyecto.descripcion), (p.idProyecto.fechaInicio).strftime('%d/%m/%Y'), (p.idProyecto.fechaFin).strftime('%d/%m/%Y'),
            Image(p.idProyecto.idCategoria.foto)) for p in Participa.objects.order_by('-id')
            if p.idCliente.idUsuario.username == usuario_cliente]
        datos_pry = Table([encabezados] + datos, colWidths=[4*cm,4*cm,4*cm], splitByRow = True)
        datos_pry.setStyle(TableStyle(
            [
                ('ALIGN',(0,0),(6,10),'CENTER'),
                ('GRID', (0,0),(4,0),1, colors.transparent),
                ('FONTSIZE', (0,0),(-1,-1),10),
                ('BACKGROUND',(0,0),(-1,-1),colors.Color(red=(250/255),green=(128/255),blue=(114/255), alpha=(125/255))),
                ('COLBACKGROUNDS',(0,1),(-1,-1),(colors.beige,colors.lightyellow)),
                
            ]
        ))
        
    
        datos_pry.wrapOn(cliente_pdf,800,600)
        datos_pry.drawOn(cliente_pdf,10,posicion_y)
        return datos_pry
    
    
    def get(self, request, cliente_id, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="informe_cliente.pdf"'    
        
        buffer = BytesIO()
        cliente_pdf = canvas.Canvas(buffer, pagesize=A4)
        
        self.header(cliente_pdf)
        
        id_cliente = Cliente.objects.filter(id=cliente_id)
        posicion_cliente_y = 680
        self.tabla_datos_cliente(cliente_pdf,posicion_cliente_y, id_cliente)
        
        posicion_proyectos_y = 323
        self.tabla_proyectos_cliente(cliente_pdf,posicion_proyectos_y, request.user.username)
        
        cliente_pdf.showPage()
        cliente_pdf.save()
        
        cliente_pdf = buffer.getvalue()
        buffer.close()
        response.write(cliente_pdf)
        return response