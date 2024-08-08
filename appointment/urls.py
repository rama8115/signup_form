from django.urls import path
from .views import doctor_list, book_appointment, appointment_details
from . import views

urlpatterns = [
    path('doctors/', doctor_list, name='doctor_list'),
    path('book/<int:doctor_id>/', book_appointment, name='book_appointment'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    path('details/<int:appointment_id>/', appointment_details, name='appointment_details'),
]
