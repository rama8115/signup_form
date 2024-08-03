from django.urls import path
from .views import create_blog_post, doctor_blog_list, patient_blog_list, patient_blog_category

urlpatterns = [
    path('create_blog_post/', create_blog_post, name='create_blog_post'),
    path('doctor_blog_list/', doctor_blog_list, name='doctor_blog_list'),
    path('patient_blog_list/', patient_blog_list, name='patient_blog_list'),
    path('patient_blog_list/category/<int:category_id>/', patient_blog_category, name='patient_blog_category'),
]