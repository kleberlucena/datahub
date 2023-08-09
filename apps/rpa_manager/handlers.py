from django.shortcuts import render
from functools import wraps

def require_permission(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.has_perm('rpa_manager.delete_checklist'):
            return render(request, '403.html')  # Redirecionar para a página de permissão negada
        return view_func(request, *args, **kwargs)
    return _wrapped_view