import re

from users.models import User


def parse_nicknames(value):
    def pk_to_nickname(mo):
        pk = mo.group(1)
        user = User.objects.get(pk=pk)
        return '@[%s](' % user.nickname

    return re.sub(r'@\[([0-9]+)\]\(', pk_to_nickname, value)
