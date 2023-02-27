from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from src.CompanyLicense.models import Company
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from config.settings import SECRET_KEY
import json


key = bytes(SECRET_KEY, "utf-8")

cipher = AES.new(key, AES.MODE_ECB)


def validate_license(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        try:
            license = Company.objects.get(user=request.user)
            if not license.is_valid():
                return redirect('license_expired')
        except Company.DoesNotExist:
            return redirect('license_required')
        return view_func(request, *args, **kwargs)

    return wrapper


def decrypt_string(data):
    data = base64.b64decode(data.encode())
    plaintext = cipher.decrypt(data)
    plaintext = unpad(plaintext, AES.block_size)
    data = json.loads(plaintext.decode())
    return data

