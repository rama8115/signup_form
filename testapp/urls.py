from django.urls import path
from testapp import views 

urlpatterns = [
     path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
]