from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db.models import Q

User = get_user_model()


def authenticate(phone, password):
    user = User.objects.filter(Q(phone=phone)).first()
    if user:
        is_user = check_password(password, user.password)
        if is_user:
            return user
        else:
            return None
    else:
        return None
