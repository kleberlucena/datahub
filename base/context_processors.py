from django.conf import settings

def portal_url(request):
    return {'URL_PORTAL': settings.PORTAL_URL_BASE}