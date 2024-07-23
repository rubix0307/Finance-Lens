from django.urls import path

from . import views

urlpatterns = [
    path('web-app/', views.check, name='redirect_web_app'),
    path('authenticate/', views.authenticate_web_app, name='authenticate_web_app'),
]
