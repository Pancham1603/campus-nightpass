from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path('api/users', check_user),
    path('api/users/update', update_user_image),
]
