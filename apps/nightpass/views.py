from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import *
from ..users.models import *
from ..global_settings.models import Settings as settings
import random
import string
import json
from datetime import date, time, datetime
import random, string
from .models import *
from ..users.views import *
from datetime import datetime, date, timedelta


@login_required
def campus_resources_home(request):
    Settings = settings.objects.first()
    campus_resources = CampusResource.objects.filter(is_display=True)
    user = request.user
    if user.user_type == 'student':
        user_pass = NightPass.objects.filter(user=user, valid=True).first()
        user_incidents = NightPass.objects.filter(user=user, defaulter=True)
        
        if Settings.enable_hostel_timers:
            checkin_timer = user.student.hostel.frontend_checkin_timer
        else:
            checkin_timer = Settings.frontend_checkin_timer
        announcement = Settings.announcement if Settings.announcement else False
        return render(request, 'lmao.html', {'user':user.student,'campus_resources':campus_resources, 'user_pass':user_pass, 'user_incidents':user_incidents, 'frontend_checkin_timer':checkin_timer, 'announcement':announcement, 'valid_entry_without_checkout':Settings.valid_entry_without_hostel_checkout})	
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
                'message':'Booking is currently not available for this resource.'
                }
        return HttpResponse(json.dumps(data))

    if campus_resource.booking_complete:
        data = {
                'status':False,
                'message':'All slots are booked for today!'
                }
        return HttpResponse(json.dumps(data))
    
    Settings = settings.objects.first()

    if int(user.student.violation_flags) >= int(Settings.max_violation_count):
        data = {
                'status':False,
                'message':'Nightpass facility has been temporarily suspended! Contact DOSA office for further details.'
                }
        return HttpResponse(json.dumps(data))

    if Settings.enable_gender_ratio:
        if user.student.gender == 'male':
            male_pass_count = NightPass.objects.filter(valid=True, campus_resource=campus_resource,
                                                        user__student__gender='male').count()
            if (male_pass_count > Settings.male_ratio*(campus_resource.max_capacity)) or Settings.male_ratio==float(0):
                data = {
                'status':False,
                'message':'All slots are booked for today!'
                }
                return HttpResponse(json.dumps(data))

        elif user.student.gender == 'female':
            female_pass_count = NightPass.objects.filter(valid=True, campus_resource=campus_resource, 
                                                         user__student__gender='female').count()
            if (female_pass_count > Settings.female_ratio*(campus_resource.max_capacity)) or Settings.female_ratio==float(0) :
                data = {
                'status':False,
                'message':'All slots are booked for today!'
                }
                return HttpResponse(json.dumps(data))
    
    if Settings.enable_yearwise_limits:
        data = {
                'status':False,
                'message':'All slots are booked for today!'
                }
        student_year = int(user.student.year)
        if student_year == 1:
            student_year_pass_count = NightPass.objects.filter(valid=True, campus_resource=campus_resource, 
                                                         user__student__year='1').count()
            if student_year_pass_count >= Settings.first_year:
                return HttpResponse(json.dumps(data))
        elif student_year == 2:
            student_year_pass_count = NightPass.objects.filter(valid=True, campus_resource=campus_resource, 
                                                         user__student__year='2').count()
            if student_year_pass_count >= Settings.second_year:
                return HttpResponse(json.dumps(data))
        elif student_year == 3:
            student_year_pass_count = NightPass.objects.filter(valid=True, campus_resource=campus_resource, 
                                                         user__student__year='3').count()
            if student_year_pass_count >= Settings.third_year:
                return HttpResponse(json.dumps(data))
        elif student_year == 4:
            student_year_pass_count = NightPass.objects.filter(valid=True, campus_resource=campus_resource, 
                                                         user__student__year='4').count()
            if student_year_pass_count >= Settings.fourth_year:
                return HttpResponse(json.dumps(data))
            
    if Settings.enable_hostel_limits:
        student_hostel_pass_count = NightPass.objects.filter(valid=True, campus_resource=campus_resource, 
                                                         user__student__hostel=user.student.hostel).count()
        if student_hostel_pass_count >= user.student.hostel.max_students_allowed:
            data = {
                'status':False,
                'message':'All slots are booked for today!'
                }
            return HttpResponse(json.dumps(data))


    user_pass = NightPass.objects.filter(user=user, date=date.today()).first()
    if not user_pass:
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
    elif user_pass.valid:
        if user_pass.check_in:
            data={
                'status':False,
                'message':f"New slot can be booked once you exit {user_pass.campus_resource}."
            }
            return HttpResponse(json.dumps(data))
        else:
            data={
                    'status':False,
                    'message':f"Cancel the booking for {user_pass.campus_resource} to book a new slot!"
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
    user_nightpass = NightPass.objects.filter(user=user, valid=True).first()
    if not user_nightpass:
        data={
            'status':False,
            'message':f"No pass to cancel!"
        }
        return HttpResponse(json.dumps(data))
    else:
        last_time = timezone.make_aware(datetime.combine(date.today(), time(20,00)), timezone.get_current_timezone())
        if timezone.now() > last_time:
            data = {
                'status':False,
                'message':f"Cannot cancel pass after 8pm."
            }
            return HttpResponse(json.dumps(data))
        else:
            if user_nightpass.check_out or user_nightpass.check_in or user_nightpass.hostel_checkout_time:
                data={
                    'status':False,
                    'message':f"Cannot cancel pass after utilization."
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


def hostel_home(request):
    user = request.user
    if request.user.is_staff and user.user_type == 'security':
        hostel_passes = NightPass.objects.filter(valid=True, user__student__hostel=request.user.security.hostel) | NightPass.objects.filter(date=date.today(), user__student__hostel=request.user.security.hostel).order_by('check_out')
        return render(request, 'caretaker.html', {'hostel_passes':hostel_passes})
    else:
        return redirect('/access')