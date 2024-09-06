
from django.urls import path

from main import views

urlpatterns = [
    path('403/', views.permission_denied_view, name='403'),
    path('', views.index, name='index'),
    path('section/', views.show_section, name='section'),
    path('delete-receipt/<int:receipt_id>/', views.delete_receipt, name='delete_receipt'),
    path('get-section-stats/', views.get_section_stats, name='get_section_stats'),
]
