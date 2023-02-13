from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import License


def validate_license(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        try:
            license = License.objects.get(user=request.user)
            if not license.is_valid():
                return redirect('license_expired')
        except License.DoesNotExist:
            return redirect('license_required')
        return view_func(request, *args, **kwargs)
    return wrapper
