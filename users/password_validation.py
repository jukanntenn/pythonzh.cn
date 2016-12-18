from django.contrib.auth.password_validation import NumericPasswordValidator as DjangoNumericPasswordValidator
from django.core.exceptions import ValidationError


class NumericPasswordValidator(DjangoNumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                "您输入的密码为纯数字",
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return "Your password can't be entirely numeric."
