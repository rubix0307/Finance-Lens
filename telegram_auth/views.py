from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect, render

from .utils import check_webapp_signature


def check(request: WSGIRequest):
    return render(request, 'telegram_auth/check.html')

def authenticate_web_app(request: WSGIRequest):

    init_data = request.GET.get('init_data')
    is_valid, user_data = check_webapp_signature(settings.BOT_TOKEN, init_data)
    if init_data and is_valid:

        user, created = get_user_model().objects.get_or_create(
            telegram_id=user_data.id,
            defaults={
                'first_name': user_data.first_name,
                'language_code': user_data.language_code,
                'last_name': user_data.last_name,
                'username': user_data.username,
            }
        )
        login(request, user)
        return redirect('index')
    return redirect('403')
