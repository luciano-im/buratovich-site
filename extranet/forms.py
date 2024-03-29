from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from extranet.models import UserInfo


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _('¡Ops! parece que su usuario y contraseña no son validos. Inténtelo nuevamente.'),
        'inactive': _('Su cuenta aún no ha sido activada. Ingrese al link de activación que recibió por correo.'),
    }


class ExtranetClientSelectionForm(forms.Form):
    client = forms.ModelChoiceField(queryset=UserInfo.objects.all().order_by('company_name'), required=True, empty_label='- - - - - -')


class UserCreationForm(ModelForm):
    username = forms.CharField(required=True, label='Nombre de usuario')
    email = forms.EmailField(required=True, label='Direccion de email')

    class Meta:
        model = User
        fields = ('username', 'email',)
