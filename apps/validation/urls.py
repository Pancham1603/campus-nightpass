from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', scanner),
    path('checkin/', check_in),
    path('checkout/', check_out),
    path('extension/fetchuser/performtask/', kiosk_extension)
]
