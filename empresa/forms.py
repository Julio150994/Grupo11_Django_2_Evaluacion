from django import forms
from empresa.models import Usuario, Cliente


class UsuarioModelForm(forms.ModelForm):
    username = forms.CharField(required=True, help_text="Debe introducir un nombre de usuario",widget=forms.TextInput(
        attrs={'class':'form-control mb-1','placeholder':'Nombre de usuario'}))
    password = forms.CharField(required=True, help_text="Debe introducir una contraseña", widget=forms.PasswordInput(
        attrs={'class':'form-control mb-1', 'placeholder':'Password'}))
        
    class Meta:
        model = Usuario
        fields = '__all__'

    
    def clean_username(self):
        value = self.cleaned_data['username']
        
        if Usuario.objects.filter(username = value).exists():
            raise forms.ValidationError("Error. Nombre de usuario ya registrado en la base de datos.")
        return value
    
    def clean_password(self):
        value = self.cleaned_data['password']
        
        if Usuario.objects.filter(password = value) is None:
            raise forms.ValidationError("Error. Falta por introducir su contraseña.")
        return value


class ClienteModelForm(forms.ModelForm):
    dni = forms.CharField(required=True, help_text="Debe introducir un dni", widget=forms.TextInput(
        attrs={'class':'form-control mb-1', 'placeholder':'Dni'}))
    nombre = forms.CharField(required=True, help_text="Debe introducir un nombre", widget=forms.TextInput(
        attrs={'class':'form-control mb-1', 'placeholder':'Nombre'}))
    apellidos = forms.CharField(required=True, help_text="Debe introducir unos apellidos", widget=forms.TextInput(
        attrs={'class':'form-control mb-1', 'placeholder':'Apellidos'}))
    direccion = forms.CharField(required=True, help_text="Debe introducir una dirección", widget=forms.TextInput(
        attrs={'class':'form-control mb-1', 'placeholder':'Dirección'}))
    fechaNacimiento = forms.DateField(required=True, help_text="Debe seleccionar una fecha de nacimiento",widget=forms.DateInput(
        attrs={'class':'form-control mb-1', 'type':'date', 'placeholder':'Fecha de Nacimiento'}))
    fechaAlta = forms.DateField(required=True, help_text="Debe seleccionar una fecha de alta en la empresa",widget=forms.DateInput(
        attrs={'class':'form-control mb-1', 'type':'date', 'placeholder':'Fecha de Alta'}))
    
    class Meta:
        model = Cliente
        fields = ['dni','nombre','apellidos','direccion','fechaNacimiento','fechaAlta']
        
    def clean_dni(self):
        value = self.cleaned_data['dni']
        
        if Cliente.objects.filter(dni = value) is None:
            raise forms.ValidationError("Error. Debe introducir un dni")
        return value
    
    def clean_nombre(self):
        value = self.cleaned_data['nombre']
        
        if Cliente.objects.filter(nombre = value) is None:
            raise forms.ValidationError("Error. Debe introducir un nombre")
        return value
    
    def clean_apellidos(self):
        value = self.cleaned_data['apellidos']
        
        if Cliente.objects.filter(apellidos = value) is None:
            raise forms.ValidationError("Error. Debe introducir unos apellidos")
        return value
    
    def clean_direccion(self):
        value = self.cleaned_data['direccion']
        
        if Cliente.objects.filter(direccion = value) is None:
            raise forms.ValidationError("Error. Debe introducir una dirección")
        return value
    
    def clean_fecha_nacimiento(self):
        value = self.cleaned_data['fechaNacimiento']
        
        if Cliente.objects.filter(fechaNacimiento = value) is None:
            raise forms.ValidationError("Error. Debe introducir una fecha de nacimiento")
        return value
    
    def clean_fecha_alta(self):
        value = self.cleaned_data['fechaAlta']
        
        if Cliente.objects.filter(fechaAlta = value) is None:
            raise forms.ValidationError("Error. Debe introducir una fecha de alta")
        return value
