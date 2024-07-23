from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, render

from .utils import check_webapp_signature


def check(request: WSGIRequest):
    return render(request, 'telegram_auth/check.html')

def authenticate_web_app(request: WSGIRequest):

    init_data = request.GET.get('init_data')

    if init_data and check_webapp_signature(settings.BOT_TOKEN, init_data):
        # TODO auth
        return redirect('index')
    return redirect('403')
