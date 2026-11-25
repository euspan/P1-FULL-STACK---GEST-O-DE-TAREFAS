from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def papel_requerido(papel):
    def decorator(view):
        @login_required
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            perfil = getattr(request.user, 'perfil', None)
            if perfil is None or perfil.papel != papel:
                return HttpResponse('Acesso restrito ao administrador.', status=403)
            return view(request, *args, **kwargs)
        return wrapper
    return decorator
