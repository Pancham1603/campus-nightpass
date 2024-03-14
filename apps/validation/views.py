from django.shortcuts import render, HttpResponse
from ..nightpass.models import *
from ..users.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime, date, timedelta
import requests
from django.utils import timezone
# Create your views here.

def fetch_user_status(request):
    if request.method == 'POST':
        if request.user.is_staff:    
            data = request.POST
            try:
                user = Student.objects.get(registration_number=data['registration_number'])
                user_pass = NightPass.objects.filter(user=user.user, valid=True).first()
                admin_campus_resource = request.user.security.campus_resource if request.user.security.campus_resource else request.user.security.hostel
                if not user_pass:
                    data = {
                        'status':True,
                        'message':f'Pass does not exist!',
                        'user':{
                            'name':user.name,
                            'registration_number':user.registration_number,
                            'hostel':user.hostel.name if user.hostel else None,
                            'room_number':user.room_number,
                            'picture':user.picture,
                            'is_checked_in':user.is_checked_in,
                            'hostel_checkin_time':str(user.hostel_checkin_time),
                            'hostel_checkout_time':str(user.hostel_checkout_time),
                            'last_checkout_time':str(user.last_checkout_time),
                            'has_booked':user.has_booked,
                        },
                        'user_pass':{
                            'pass_id':None,
                            'campus_resource':None,
                            'check_in':None,
                            'check_out':None,
                            'check_in_time':None,
                            'check_out_time':None
                        } }
                else:
                    data = {
                        'status':True,
                        'message':'Successfully fetched!',
                        'user':{
                            'name':user.name,
                            'registration_number':user.registration_number,
                            'hostel':user.hostel.name if user.hostel else None,
                            'room_number':user.room_number,
                            'picture':user.picture,
                            'is_checked_in':user.is_checked_in,
                            'hostel_checkin_time':str(user.hostel_checkin_time),
                            'hostel_checkout_time':str(user.hostel_checkout_time),
                            'last_checkout_time':str(user.last_checkout_time),
                            'has_booked':user.has_booked,
                        },
                        'user_pass':{
                            'pass_id':user_pass.pass_id,
                            'campus_resource':user_pass.campus_resource.name,
                            'check_in':user_pass.check_in,
                            'check_out':user_pass.check_out,
                            'check_in_time':str(user_pass.check_in_time),
                            'check_out_time':str(user_pass.check_out_time),
                        }
                    }
                if type(admin_campus_resource) == Hostel:
                    data['task'] = {
                        'check_in':True if not user.is_checked_in else False,
                        'check_out':True if (user.is_checked_in and user.has_booked) else False
                    }
                    data['request_user_location'] = 'hostel'
                    return HttpResponse(json.dumps(data))
                elif type(admin_campus_resource) == CampusResource:
                    if user_pass:
                        data['task'] = {
                            'check_in':True if not user_pass.check_in else False,
                            'check_out':True if (not user_pass.check_out and user_pass.check_in) else False
                        }
                    data['request_user_location'] = 'campus_resource'
                    return HttpResponse(json.dumps(data))
                else:
                    print(213)
                    data = {
                            'status':False,
                            'message':f'Pass for {admin_campus_resource.name} does not exist!'
                            }
                    return HttpResponse(json.dumps(data))
                
            except Student.DoesNotExist:
                data = {
                        'status':False,
                        'message':'Invalid!'
                        }
                return HttpResponse(json.dumps(data))
            

def req_library_logs(registration_number):
    req = requests.session()
    url = "https://library.thapar.edu/inout/login_verify.php"
    data = {
        "name": "user",
        "pass": "$#**123",
        "loc": "TESTLIB",
        "submit": "Login"
    }
    response = req.post(url, data=data, verify=False)
    req.get(f"https://library.thapar.edu/inout/user.php?id={registration_number}")
    req.close()


@csrf_exempt
@login_required
def check_out(request):
    if request.user.is_staff:
        if request.method == 'POST':
            data = request.POST
            try:
                user = Student.objects.get(registration_number=data['registration_number'])
                user_pass = NightPass.objects.filter(user=user.user, valid=True).first()
                admin_campus_resource = request.user.security.campus_resource if request.user.security.campus_resource else request.user.security.hostel
                if not user_pass:
                    data = {
                        'status':False,
                        'message':'Pass does not exist!'
                    }
                    return HttpResponse(json.dumps(data))
                if type(admin_campus_resource) == Hostel:
                    return checkout_from_hostel(user_pass)
                elif type(admin_campus_resource) == CampusResource:
                    if admin_campus_resource.name == 'Library':
                        req_library_logs(user.registration_number)
                    return checkout_from_location(user_pass, admin_campus_resource)
            except Student.DoesNotExist:
                data = {
                        'status':False,
                        'message':'Invalid!'
                        }
                return HttpResponse(json.dumps(data))
    else:
        return HttpResponse('Invalid Operation')


def checkout_from_hostel(user_pass:NightPass, direct:bool=True):
    user = user_pass.user
    user.student.is_checked_in = False
    user.student.hostel_checkout_time = user_pass.hostel_checkout_time = datetime.now() if direct else None
    user.student.last_checkout_time = datetime.now() if direct else None
    user.student.save()
    user_pass.save()
    data = {
        'status':True,
        'message':'Successfully checked out!'
    }
    data['student_stats'] = None
    return HttpResponse(json.dumps(data))

def checkout_from_location(user_pass, admin_campus_resource:CampusResource=None ,direct:bool=True, ):
    user = user_pass.user
    if not is_repeated_scan(user_pass):
        user.student.last_checkout_time = datetime.now() if direct else None
        user.student.has_booked = False
        user.student.save()
        user_pass.check_out = True if direct else False
        user_pass.check_out_time = datetime.now() if direct else None
        user_pass.save()
        data = {
            'status':True,
            'message':'Successfully checked out!'
        }
        data['student_stats'] = {
            'check_in_count':NightPass.objects.filter(check_in=True, check_out=False,valid=True, date=date.today(), campus_resource=admin_campus_resource).count(),
            'total_count':NightPass.objects.filter(valid=True, date=date.today(), campus_resource=admin_campus_resource).count()
        }
    else:
        data = {
        'status':False,
        'repeated':True,
        'message':'You just checked in! Please wait for 10mins before checking out'
        }
        data['student_stats'] = {
            'check_in_count':NightPass.objects.filter(check_in=True, check_out=False,valid=True, date=date.today(), campus_resource=admin_campus_resource).count(),
            'total_count':NightPass.objects.filter(valid=True, date=date.today(), campus_resource=admin_campus_resource).count()
        }
    return HttpResponse(json.dumps(data))

@csrf_exempt
@login_required
def check_in(request):
    if request.user.is_staff:
        if request.method == 'POST':
            data = request.POST
            try:
                user = Student.objects.get(registration_number=data['registration_number'])
                user_pass = NightPass.objects.filter(user=user.user, valid=True).first()
                admin_campus_resource = request.user.security.campus_resource if request.user.security.campus_resource else request.user.security.hostel
                if type(admin_campus_resource) == Hostel:
                    return checkin_to_hostel(user)
                elif type(admin_campus_resource) == CampusResource:
                    if not user_pass:
                        data = {
                            'status':False,
                            'message':'Pass does not exist!'
                        }
                        return HttpResponse(json.dumps(data))
                    if admin_campus_resource.name == 'Library':
                        req_library_logs(user.registration_number)
                    return checkin_to_location(user_pass, admin_campus_resource)
            except Student.DoesNotExist:
                data = {
                        'status':False,
                        'message':'Invalid!'
                        }
                return HttpResponse(json.dumps(data))
    else:
        return HttpResponse('Invalid Operation')

def checkin_to_hostel(user:Student):
    if not user.is_checked_in:
        user_pass = NightPass.objects.filter(user=user.user, valid=True).first()
        if not is_repeated_scan(user_pass):
            user.is_checked_in = True
            user.hostel_checkin_time = user_pass.hostel_checkin_time= datetime.now()
            user.save()
            user_pass.valid = False
            user_pass.save()
            if (not user_pass.check_out if user_pass else False):
                checkout_from_location(user_pass,admin_campus_resource=user_pass.campus_resource ,direct=False)
            data = {
                'status':True,
                'message':'Successfully checked in!'
            }
            data['student_stats'] = None

            return HttpResponse(json.dumps(data))
        else:
            data = {
                'status':False,
                'message':'You just checked out! Please wait for 10mins before checking in again'
            }
            return HttpResponse(json.dumps(data))
    else:
        data = {
            'status':False,
            'message':'Already checked in!'
        }
        return HttpResponse(json.dumps(data))

def checkin_to_location(user_pass, admin_campus_resource:CampusResource):
    user = user_pass.user
    if user.student.is_checked_in:
        checkout_from_hostel(user_pass, direct=False)
    user_pass.check_in = True
    user_pass.check_in_time = datetime.now()
    user_pass.save()
    data = {
        'status':True,
        'message':'Successfully checked in!'
    }
    data['student_stats'] = {
        'check_in_count':NightPass.objects.filter(check_in=True, check_out=False,valid=True, date=date.today(), campus_resource=admin_campus_resource).count(),
        'total_count':NightPass.objects.filter(valid=True, date=date.today(), campus_resource=admin_campus_resource).count()
    }
    return HttpResponse(json.dumps(data))

@csrf_exempt
@login_required
def scanner(request):
    if request.method == "POST":
        return fetch_user_status(request)
    if request.user.is_staff:
        if request.user.security.campus_resource:
            check_in_count = NightPass.objects.filter(check_in=True, check_out=False,valid=True, date=date.today(), campus_resource=request.user.security.campus_resource).count()
            total_count = NightPass.objects.filter(valid=True, date=date.today(), campus_resource=request.user.security.campus_resource).count()
            return render(request, 'info.html', {'check_in_count':check_in_count, 'total_count':total_count})
        elif request.user.security.hostel:
            return render(request, 'info.html', {'check_in_count':None, 'total_count':None})
    else:
        return HttpResponse('Invalid Operation')
    

def is_repeated_scan(user_pass:NightPass):
    if (user_pass.check_in and not user_pass.check_out) and (timezone.make_aware(datetime.now(), timezone.get_current_timezone())-user_pass.check_in_time<timedelta(minutes=10)):
        return True
    elif (user_pass.hostel_checkout_time) and (timezone.make_aware(datetime.now(), timezone.get_current_timezone())-user_pass.hostel_checkout_time<timedelta(minutes=10)):
        return True
    else: 
        return False



@csrf_exempt
def kiosk_extension(request):
    if request.user.is_staff:
        data = request.GET
        try:
            user = Student.objects.get(registration_number=data['registration_number'])
            user_pass = NightPass.objects.filter(user=user.user, valid=True).first()
            admin_campus_resource = request.user.security.campus_resource if request.user.security.campus_resource else request.user.security.hostel
            if user_pass:
                data = {
                    'status':True,
                    'message':'Successfully fetched!',
                    'user':{
                        'name':user.name,
                        'registration_number':user.registration_number,
                        'hostel':user.hostel.name if user.hostel else None,
                        'room_number':user.room_number,
                        'picture':user.picture,
                        'is_checked_in':user.is_checked_in,
                        'hostel_checkin_time':str(user.hostel_checkin_time),
                        'hostel_checkout_time':str(user.hostel_checkout_time),
                        'last_checkout_time':str(user.last_checkout_time),
                        'has_booked':user.has_booked,
                    },
                    'user_pass':{
                        'pass_id':user_pass.pass_id,
                        'campus_resource':user_pass.campus_resource.name,
                        'check_in':user_pass.check_in,
                        'check_out':user_pass.check_out,
                        'check_in_time':str(user_pass.check_in_time),
                        'check_out_time':str(user_pass.check_out_time),
                    }
                }
                if type(admin_campus_resource) == Hostel:
                    if not user.is_checked_in:
                        checkin_to_hostel(user)
                        data['colour'] = '#ffff80'
                    else:
                        checkout_from_hostel(user_pass)
                        data['colour'] = '#8aff8a'
                    return render('extension.html', {'data':data})
                elif type(admin_campus_resource) == CampusResource and admin_campus_resource == (user_pass.campus_resource if user_pass else None):
                    if not user_pass.check_in:
                        checkin_to_location(user_pass)
                        data['colour'] = '#8aff8a'
                    elif not user_pass.check_out and user_pass.check_in:
                        checkout_from_location(user_pass)
                        data['colour'] = '#ffff80'
                    return render('extension.html', {'data':data})
                return 
            else:
                data = {
                    'status':False,
                    'message':'Pass does not exist!'
                }
                return render('extension.html', {'data':data})
        except Student.DoesNotExist:
            data = {
                    'status':False,
                    'message':'Invalid!'
                    }
            return render('extension.html', {'data':data})

