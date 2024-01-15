import logging
from allauth.socialaccount.models import SocialToken, SocialApp, SocialAccount
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.account.signals import user_signed_up
from allauth.account.models import EmailAddress
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from django.contrib import auth, messages
import requests

from . import helpers

logger = logging.getLogger(__name__)


class PMPBSocialAccountAdapter(DefaultSocialAccountAdapter):
    @csrf_exempt
    def get_logout_redirect_url(self, request):
        if request.user.is_authenticated:
            user = request.user
            if SocialToken.objects.filter(account__user=user).exists():
                social = SocialToken.objects.get(account__user=user)
                access_token = social.token
                refresh_token = social.token_secret
                social_app = SocialApp.objects.all().first()
                keycloak_url = settings.KEYCLOAK_URL
                realm_name = settings.KEYCLOAK_REALM
                logout_url = (
                    f"{keycloak_url}/realms/{realm_name}/protocol/openid-connect/logout"
                )
                logout_request_data = {
                    "client_id": social_app.client_id,
                    "refresh_token": refresh_token,
                    "client_secret": social_app.secret,
                }
                headers = {
                    "Authorization": "Bearer " + access_token,
                    "Content-Type": "application/x-www-form-urlencoded",
                }
                requests.post(logout_url, data=logout_request_data, headers=headers)
        return reverse("base:index")

    def is_auto_signup_allowed(self, request, sociallogin):
        try:
            user = User.objects.get(username=sociallogin.user.username)
        except User.DoesNotExist:
            logger.warning(
                "[AUTH OIDC] - User {} will be created".format(
                    sociallogin.user.username
                )
            )
            return super().is_auto_signup_allowed(request, sociallogin)

        # busca o SocialToken associado ao usuário
        try:
            social_account = SocialAccount.objects.get(user=user)
            social_token = SocialToken.objects.get(account__user=user)
            # remove o SocialToken existente
            social_token.delete()
            social_account.delete()
            logger.warning(
                "[AUTH OIDC] - User {} will be updated".format(
                    sociallogin.user.username
                )
            )
        except (SocialAccount.DoesNotExist, SocialToken.DoesNotExist):
            pass

        sociallogin.connect(request, user)
        messages.info(
            self.request,
            "Seu usuário foi atualizado com sucesso para novo sistema de autenticação - SSO.",
        )
        return False

    def pre_social_login(self, request, sociallogin):
        if sociallogin.user.id:
            helpers.synchronize_oidc_permission(sociallogin.user, request)
            if not sociallogin.user.groups.filter(name="feature:authenticate").exists():
                auth.logout(request)
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Você não tem as permissões necessárias para esse sistema, caso precise entre em contato com o suporte técnico através do Portal de Aplicativos...",
                )
                # Lançar a exceção para interromper o processo de login e redirecionar para a página desejada
                raise ImmediateHttpResponse(
                    HttpResponseRedirect(reverse("auth_oidc:info_user_inactivate"))
                )

            # Verifica se o e-mail mudou e atualiza
            user = User.objects.filter(username=sociallogin.user.username).first()
            if user.email != sociallogin.account.extra_data["email"]:
                old_email = user.email
                new_email = sociallogin.account.extra_data["email"]
                user.email = new_email
                user.save()
                # Atualiza ou cria o objeto EmailAddress
                email_address, created = EmailAddress.objects.get_or_create(
                    user=user, email=old_email
                )
                email_address.email = new_email
                email_address.verified = True  # Marca como verificado se for desejado
                email_address.primary = True
                email_address.save()
                logger.warning(
                    f"[AUTH OIDC] - Email updated for user {user.username} from {old_email} to {new_email}"
                )
        super().pre_social_login(request, sociallogin)


@receiver(user_signed_up)
def post_signup(sender, user, request, **kwargs):
    helpers.synchronize_oidc_permission(user, request)
    if not user.groups.filter(name="feature:authenticate").exists():
        auth.logout(request)
        messages.add_message(
            request,
            messages.ERROR,
            "Você não tem as permissões necessárias para esse sistema, caso precise entre em contato com o suporte técnico através do Portal de Aplicativos...",
        )
        # Lançar a exceção para interromper o processo de login e redirecionar para a página desejada
        raise ImmediateHttpResponse(
            HttpResponseRedirect(reverse("auth_oidc:info_user_inactivate"))
        )
