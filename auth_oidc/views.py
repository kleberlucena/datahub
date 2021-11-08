from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import auth
import urllib.parse as encode
from django.urls import reverse_lazy
# from django.urls import reverse
# from allauth.account.views import LoginView


def logout(request):
    """
    Realize logout from system local e redirect to logout on provider OIDC
    :param request:
    :return HttpResponseRedirect:
    """

    url = settings.OIDC_OP_LOGOUT_ENDPOINT
    uri = encode.quote(settings.ACCOUNT_LOGOUT_REDIRECT_URL)
    keycloak_redirect = url + "?redirect_uri=" + uri

    if request.user.is_authenticated:
        auth.logout(request)

    return HttpResponseRedirect(keycloak_redirect)  # redirect to provider OIDC
