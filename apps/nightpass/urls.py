from django.urls import path
from . import views

urlpatterns = [
    path('', views.campus_resources_home),
    path('book/<str:campus_resource>', views.generate_pass),
    path('cancel/', views.cancel_pass),
    path('hostel/', views.hostel_home),
    path('defaulter_notification/', views.remove_defaulter_notif),
    ]
