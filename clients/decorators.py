from django.shortcuts import redirect
from django.urls import reverse

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # لو مش عامل تسجيل دخول → وده لصفحة تسجيل الدخول ومعاه next
                login_url = reverse('login')
                return redirect(f"{login_url}?next={request.path}")

            # لو عامل تسجيل دخول لكن نوع الحساب مش مسموح
            if request.user.user_type not in allowed_roles:
                return redirect('no_permission')

            # لو مسموح يدخل
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
