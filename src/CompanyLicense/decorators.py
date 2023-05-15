from datetime import date
from functools import wraps

from django.http import HttpResponseBadRequest
from django.shortcuts import redirect

from src.CompanyLicense.models import Company
from src.CameraAlgorithms.models import Camera
from src.CameraAlgorithms.models import CameraAlgorithm


def validate_license(view_func):
    """
    The decorator is used to check if a company's license is active
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        company = Company.objects.last()
        if not company.is_active or date.today() > company.valid_until:
            return redirect("license expired")
        return view_func(request, *args, **kwargs)

    return wrapper


def check_active_cameras(view_func):
    """
    A decorator for checking the number of active cameras a company has.
    """

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        company = Company.objects.last()

        if not company.is_active:
            return HttpResponseBadRequest("Your license is inactive.")

        active_cameras_count = Camera.objects.filter(is_active=True).count()
        if active_cameras_count >= company.count_cameras:
            return HttpResponseBadRequest(
                "You have exceeded the limit of active cameras."
            )

        return view_func(request, *args, **kwargs)

    return wrapped_view


def check_active_algorithms(view_func):
    """
    Decorator to check if at least one of the algorithms in the company's
    list of active neurons is present in the requested view's list of allowed
    algorithms
    """

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        company = Company.objects.last()

        if not company.is_active:
            return HttpResponseBadRequest("Your license is inactive.")

        active_algorithms_count = (
            CameraAlgorithm.objects.values("algorithm_id").distinct().count()
        )
        if active_algorithms_count >= company.neurons_active:
            return HttpResponseBadRequest(
                "You have exceeded the limit of active algorithm."
            )

        return view_func(request, *args, **kwargs)

    return wrapped_view
