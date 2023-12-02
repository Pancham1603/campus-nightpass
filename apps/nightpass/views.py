from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from .models import *
from ..users.models import *
import random
import string
import json
from datetime import date, time, datetime
import random, string
from .models import *
from ..users.views import *
from datetime import datetime
import json
from django.db.utils import IntegrityError


@login_required
def campus_resources_home(request):
    campus_resources = CampusResource.objects.filter(is_display=True)
    user = request.user
    if user.user_type == 'student':
        user_pass = NightPass.objects.filter(user=user, check_out=False).first()
        return render(request, 'lmao.html', {'user':user.student,'campus_resources':campus_resources, 'user_pass':user_pass})	
    elif user.user_type == 'security':
        return redirect('/access')
    elif user.user_type == 'admin':
        return redirect('/admin')

@csrf_exempt
@login_required
def generate_pass(request, campus_resource):
    user = request.user
    campus_resource = CampusResource.objects.get(name=campus_resource)
    
    if (campus_resource.is_display == False) or not campus_resource.is_booking:
        data = {
                'status':False,
                'message':'Booking is currently not available for this resource'
                }
        return HttpResponse(json.dumps(data))

    if campus_resource.booking_complete:
        data = {
                'status':False,
                'message':'No slots available!'
                }
        return HttpResponse(json.dumps(data))
    
    user_pass = NightPass.objects.filter(user=user, date=date.today()).first()
    if not user.student.has_booked and not user_pass:
            campus_resource.refresh_from_db()
            if campus_resource.slots_booked < campus_resource.max_capacity:
                while True:
                    pass_id = ''.join(random.choices(string.ascii_uppercase +
                                        string.digits, k=16))

                    if not NightPass.objects.filter(pass_id=pass_id).count():
                        break
                generated_pass = NightPass(campus_resource=campus_resource, pass_id=pass_id, user=user , date=date.today(), start_time=datetime.now(), end_time=datetime.now())
                generated_pass.save()

                user.student.has_booked = True
                campus_resource.slots_booked += 1
                user.student.save()
                campus_resource.save()
                data = {
                    'pass_qr':None,
                    'status':True,
                    'message':f"Pass generated successfully for {campus_resource.name}!"
                }
                return HttpResponse(json.dumps(data))
            else:
                data={
                    'status':False,
                    'message':f"No more slots available for {campus_resource.name}!"
                }
                return HttpResponse(json.dumps(data))
    elif user.student.has_booked:
        user_nightpass = NightPass.objects.filter(user=user, check_out = False).first()
        if user_nightpass.check_in:
            data={
                'status':False,
                'message':f"New slot can be booked once you exit {user_nightpass.campus_resource}."
            }
            return HttpResponse(json.dumps(data))
        else:
            data={
                    'status':False,
                    'message':f"Cancel the booking for {user_nightpass.campus_resource} to book a new slot!"
                }
            return HttpResponse(json.dumps(data))
    elif user_pass:
        data={
                'status':False,
                'message':f"Pass already generated for today!"
            }
        return HttpResponse(json.dumps(data))


@csrf_exempt
@login_required
def cancel_pass(request):
    user = request.user
    user_nightpass = NightPass.objects.filter(user=user, check_in=False).first()
    user_nightpass = user_nightpass if user_nightpass else NightPass.objects.filter(user=user).first()
    if not user_nightpass:
        data={
            'status':False,
            'message':f"No pass to cancel!"
        }
        return HttpResponse(json.dumps(data))
    if user_nightpass.check_out and user_nightpass.check_in:
        data={
            'status':False,
            'message':f"Cannot cancel pass after utilization."
        }
        return HttpResponse(json.dumps(data))
    elif user_nightpass.check_in:
        data={
            'status':False,
            'message':f"Cannot cancel pass once you enter {user_nightpass.campus_resource}."
        }
        return HttpResponse(json.dumps(data))
    else:
        user_nightpass.delete()
        user_nightpass.campus_resource.slots_booked -= 1
        user_nightpass.campus_resource.save()
        user.student.has_booked = False
        user.student.save()
        data={
            'status':True,
            'message':f"Pass cancelled successfully!"
        }
        return HttpResponse(json.dumps(data))
