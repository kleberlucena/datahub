
from django.shortcuts import redirect
from django.contrib import auth
from django.views.generic import TemplateView
from allauth.socialaccount.adapter import get_adapter

from .tasks import task_update_social_account_from_user

class InfoUserInactivateView(TemplateView):
    """Show info to user inactivate"""
    template_name = 'account/account_inactive.html'


class ComandsAPIAuthOidcView(TemplateView):
    template_name = 'command_auth_oidc.html'
    
    
class TaskUpdateSocialAccountsView(TemplateView):
    template_name = 'process_task_update_social_accounts.html'

    def get_context_data(self, **kwargs):
        context = super(TaskUpdateSocialAccountsView,
                        self).get_context_data(**kwargs)
        task = task_update_social_account_from_user.delay()
        context['task_id'] = task.id
        return context
    

def logout(request):
    adapter = get_adapter(request)
    logout_url = adapter.get_logout_redirect_url(request)
    auth.logout(request)
    return redirect(logout_url)
