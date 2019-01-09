from django.contrib.auth import authenticate, login
from app_authentication.models import User

def authenticated_user(username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        try:
            logged_user = User.objects.get(username=username)
            if logged_user.status == User.STATUS_ACTIVATED:
                return user, ''
            else:
                return None, 'Tài khoản đã bị khóa'
        except User.DoesNotExist:
            pass
        return None, "Thông tin người dùng hoặc mật khẩu không hợp lệ"
    else:
        return None, "Thông tin người dùng hoặc mật khẩu không hợp lệ"


def login_user(request, user):
    login(request, user)
    return user