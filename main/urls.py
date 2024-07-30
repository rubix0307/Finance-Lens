
from django.urls import path

from main import views

urlpatterns = [
    path('403/', views.permission_denied_view, name='403'),
    path('', views.index, name='index'),
    path('delete-receipt/<int:receipt_id>/', views.delete_receipt, name='delete_receipt'),
    path('get-user-stats/', views.get_user_stats, name='get_user_stats'),
]
