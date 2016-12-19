from django.contrib.auth.validators import ASCIIUsernameValidator as DjangoASCIIUsernameValidator


class ASCIIUsernameValidator(DjangoASCIIUsernameValidator):
    regex = r'^[\w]+$'
    message = '用户名只能包含数字和字母'
