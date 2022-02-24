from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect

from empresa.models import Usuario


def EmpleadoDeco(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='users_login'):
   
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff and not u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def ClienteDeco(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='users_login'):
   
    actual_decorator = user_passes_test(
        lambda u: u.is_active and not u.is_superuser and not u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def Admin(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='users_login'):
       
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator