from functools import wraps
from base.views import authorization_error_view

def require_permission(permission_required):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.has_perm(permission_required):
                return authorization_error_view(request)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator