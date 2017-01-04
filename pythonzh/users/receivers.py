from django.utils import timezone


def update_last_login(sender, request, user, **kwargs):
    user.last_login = timezone.now()
    user.last_login_ip = request.META.get("REMOTE_ADDR", None)
    user.save(update_fields=['last_login', 'last_login_ip'])
    print(user.last_login, user.last_login_ip)


def update_joined(sender, request, user, **kwargs):
    user.ip_joined = request.META.get("REMOTE_ADDR", None)
    user.save(update_fields=['ip_joined'])
    print(user.ip_joined)
