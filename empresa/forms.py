from django import forms
from empresa.models import Usuario, Cliente

class UsuarioModelForm(forms.ModelForm):
    username = forms.CharField(required=True, help_text="Debe introducir un nombre de usuario",widget=forms.TextInput(
        attrs={'class':'form-control mb-1','placeholder':'Enter your username'}))
    password = forms.CharField(required=True, help_text="Debe introducir una contraseña", widget=forms.PasswordInput(
        attrs={'class':'form-control mb-1', 'placeholder':'Enter your password'}))
        
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
