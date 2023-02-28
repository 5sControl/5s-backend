from functools import wraps
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from src.CompanyLicense.models import Company
from src.Cameras.models import Camera
from src.Algorithms.models import Algorithm


def validate_license(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        try:
            company = Company.objects.last()
            if not company.is_active:
                return HttpResponse('License is not active')
            elif company.count_cameras <= Camera.objects.filter(is_active=True).count():
                return HttpResponse('Limit of active cameras has been reached')
            elif not all(algorithm.is_available for algorithm in
                         Algorithm.objects.filter(name__in=company.neurons_active.split(','))):
                return HttpResponse('Some required algorithms are not available')
        except Company.DoesNotExist:
            return HttpResponse('License not found')
        return view_func(request, *args, **kwargs)

    return wrapper


def check_active_cameras_count(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        company = Company.objects.last()
        active_cameras_count = Camera.objects.filter(is_active=True).count()
        if active_cameras_count > company.count_cameras:
            return HttpResponseForbidden("You have exceeded the number of active cameras")
        return view_func(request, *args, **kwargs)

    return wrapper


def check_algorithm_available(algorithm_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            company = Company.objects.last()
            if algorithm_name not in company.neurons_active:
                return HttpResponseForbidden("You don't have access to this algorithm")
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
