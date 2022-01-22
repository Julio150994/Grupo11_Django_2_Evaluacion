from django import forms
from empresa.models import Categoria, Empleado, Proyecto, Usuario, Cliente

class UsuarioModelForm(forms.ModelForm):
    username = forms.CharField(required=True, help_text="Debe introducir un nombre de usuario",widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'Enter your username'}))
    password = forms.CharField(required=True, help_text="Debe introducir una contraseña", widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'Enter your password'}))
        
    class Meta:
        model = Usuario
        fields = '__all__'

class ClienteModelForm(forms.ModelForm):
    dni = forms.CharField(required=True, help_text="Debe introducir un dni", widget=forms.TextInput(
        attrs={'class':'form-control mb-1', 'placeholder':'Enter your dni'}))
    nombre = forms.CharField(required=True, help_text="Debe introducir un nombre", widget=forms.TextInput(
        attrs={'class':'form-control mb-1', 'placeholder':'Enter your name'}))
    apellidos = forms.CharField(required=True, help_text="Debe introducir unos apellidos", widget=forms.TextInput(
        attrs={'class':'form-control mb-1', 'placeholder':'Enter your apes'}))
    direccion = forms.CharField(required=True, help_text="Debe introducir una dirección", widget=forms.TextInput(
        attrs={'class':'form-control mb-1', 'placeholder':'Enter your direction'}))
    fechaNacimiento = forms.DateField(required=True, help_text="Debe seleccionar una fecha de nacimiento",widget=forms.DateInput(
        attrs={'class':'form-control mb-1', 'type':'date', 'placeholder':'Enter your date of birth'}))
    fechaAlta = forms.DateField(required=True, help_text="Debe seleccionar una fecha de alta en la empresa",widget=forms.DateInput(
        attrs={'class':'form-control mb-1', 'type':'date', 'placeholder':'Enter your discharge date'}))
    
    class Meta:
        model = Cliente
        fields = ['dni','nombre','apellidos','direccion','fechaNacimiento','fechaAlta']
        
        
class EmpleadoModelForm(forms.ModelForm):
    dni = forms.CharField(required=True, help_text="Debe introducir un dni", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Escriba su dni'}))
    nombre = forms.CharField(required=True, help_text="Debe introducir un nombre", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Escriba su nombre'}))
    apellidos = forms.CharField(required=True, help_text="Debe introducir unos apellidos", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Escriba sus apellidos'}))
    direccion = forms.CharField(required=True, help_text="Debe introducir una dirección", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Escriba su dirección'}))
    biografia = forms.CharField(required=True, help_text="Debe introducir su biografía", widget=forms.Textarea(
        attrs={'class':'form-control', 'placeholder':'Escriba su biografía'}))
    
    class Meta:
        model = Empleado
        fields = ['dni','nombre','apellidos','direccion','biografia']
        
        
class CategoriaModelForm(forms.ModelForm):
    nombre = forms.CharField(required=True, help_text="Debe introducir un nombre de categoría", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Escriba un nombre'}))
    foto = forms.ImageField(required=True, help_text="Debe seleccionar una imágen para la categoría")
    
    class Meta:
        model = Categoria
        fields = ['nombre','foto']

class ProyectoModelForm(forms.ModelForm):
    titulo = forms.CharField(required=True, help_text="Introduzca nombre del proyecto", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Escriba un nombre'}))
    descripcion = forms.CharField(required=True, help_text="Introduzca descripcion del proyecto", widget=forms.Textarea(
        attrs={'class':'form-control', 'placeholder':'Escriba una descripcion'}))
    nivel = forms.IntegerField(required=True, help_text="Introduzca nivel del proyecto", widget=forms.NumberInput(
        attrs={'class':'form-control', 'placeholder':'Escriba un nivel'}))
    fechaInicio = forms.DateField(required=True, help_text="Introduzca nombre del proyecto", widget=forms.DateInput(
        attrs={'class':'form-control','type':'date', 'placeholder':'Escriba fecha comienzo'}))
    fechaFin = forms.DateField(required=True, help_text="Introduzca nombre del proyecto", widget=forms.DateInput(
        attrs={'class':'form-control', 'type':'date', 'placeholder':'Escriba fecha fin'}))
    informeFinal = forms.CharField(required=True, help_text="Introduzca el informe final", widget=forms.Textarea(
        attrs={'class':'form-control', 'placeholder':'Escriba un informe'}))

    class Meta:
        model = Proyecto
        fields = ['titulo','descripcion','nivel','fechaInicio','fechaFin','informeFinal']
    
        