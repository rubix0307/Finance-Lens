
from django.urls import path

from main import views

urlpatterns = [
    path('403/', views.permission_denied_view, name='403'),
    path('', views.index, name='index'),
]
