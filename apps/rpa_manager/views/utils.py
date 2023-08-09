
from django.contrib.auth.models import Permission

def verify_user_permissions(self, request):
    user = self.request.user
    # Obtém todas as permissões do usuário
    user_permissions = user.user_permissions.all()
    group_permissions = Permission.objects.filter(group__user=user)

    # Mescla as permissões individuais e do grupo
    all_permissions = user_permissions | group_permissions

    # Imprime todas as permissões
    for permission in all_permissions:
        print(f"Permissão: {permission.name}, Código: {permission.codename}")