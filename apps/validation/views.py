from django.shortcuts import render, HttpResponse
from ..nightpass.models import *
from ..users.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime

# Create your views here.

def fetch_user_status(request):
    if request.method == 'POST':
        data = request.POST
        try:
            user = Student.objects.get(registration_number=data['registration_number'])
            user_pass = NightPass.objects.filter(user=user, check_out=False).first()
            admin_campus_resource = CampusResource.objects.filter(name=data['admin_campus_resource']).first()
            if not admin_campus_resource:
                admin_campus_resource = Hostel.objects.filter(name=data['admin_campus_resource']).first()
            if not user_pass:
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
                    'check_out':True if user.is_checked_in else False
                }
                return HttpResponse(json.dumps(data))
            elif type(admin_campus_resource) == CampusResource and admin_campus_resource == (user_pass.campus_resource if user_pass else None):
                data['task'] = {
                    'check_in':True if not user_pass.check_in else False,
                    'check_out':True if (not user_pass.check_out and user_pass.check_in) else False
                }
                return HttpResponse(json.dumps(data))
            else:
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

@csrf_exempt
@login_required
def check_out(request):
    if request.method == 'POST':
        data = request.POST
        try:
            user = Student.objects.get(registration_number=data['registration_number'])
            user_pass = NightPass.objects.filter(user=user, check_out=False).first()
            admin_campus_resource = CampusResource.objects.filter(name=data['admin_campus_resource']).first()
            if not admin_campus_resource:
                admin_campus_resource = Hostel.objects.filter(name=data['admin_campus_resource']).first()

            if not user_pass:
                data = {
                    'status':False,
                    'message':'Pass does not exist!'
                }
                return HttpResponse(json.dumps(data))
            if type(admin_campus_resource) == Hostel:
                return checkout_from_hostel(user_pass)
            elif type(admin_campus_resource) == CampusResource:
                return checkout_from_location(user_pass)
        except Student.DoesNotExist:
            data = {
                    'status':False,
                    'message':'Invalid!'
                    }
            return HttpResponse(json.dumps(data))
    else:
        return HttpResponse('Invalid Operation')


def checkout_from_hostel(user_pass):
    user = user_pass.user
    user.is_checked_in = False
    user.hostel_checkout_time = datetime.now()
    user.last_checkout_time = datetime.now()
    user.save()
    data = {
        'status':True,
        'message':'Successfully checked out!'
    }
    return HttpResponse(json.dumps(data))

def checkout_from_location(user_pass):
    user = user_pass.user
    user.last_checkout_time = datetime.now()
    user.has_booked = False
    user.save()
    user_pass.check_out = True
    user_pass.check_out_time = datetime.now()
    user_pass.save()
    data = {
        'status':True,
        'message':'Successfully checked out!'
    }
    return HttpResponse(json.dumps(data))

@csrf_exempt
@login_required
def check_in(request):
    if request.method == 'POST':
        data = request.POST
        try:
            user = Student.objects.get(registration_number=data['registration_number'])
            user_pass = NightPass.objects.filter(user=user, check_out=False).first()
            admin_campus_resource = CampusResource.objects.filter(name=data['admin_campus_resource']).first()
            if not admin_campus_resource:
                admin_campus_resource = Hostel.objects.filter(name=data['admin_campus_resource']).first()

            if type(admin_campus_resource) == Hostel:
                return checkin_to_hostel(user)
            elif type(admin_campus_resource) == CampusResource:
                if not user_pass:
                    data = {
                        'status':False,
                        'message':'Pass does not exist!'
                    }
                    return HttpResponse(json.dumps(data))
                return checkin_to_location(user_pass)
        except Student.DoesNotExist:
            data = {
                    'status':False,
                    'message':'Invalid!'
                    }
            return HttpResponse(json.dumps(data))
    else:
        return HttpResponse('Invalid Operation')

def checkin_to_hostel(user):
    if not user.is_checked_in:
        user.is_checked_in = True
        user.hostel_checkin_time = datetime.now()
        user.save()
        user_pass = NightPass.objects.filter(user=user, check_out=False).first()
        if (user_pass.check_in if user_pass else False):
            checkout_from_location(user_pass)
        data = {
            'status':True,
            'message':'Successfully checked in!'
        }

        return HttpResponse(json.dumps(data))
    else:
        data = {
            'status':False,
            'message':'Already checked in!'
        }
        return HttpResponse(json.dumps(data))

def checkin_to_location(user_pass):
    user = user_pass.user
    if user.is_checked_in:
        checkout_from_hostel(user_pass)
    user_pass.check_in = True
    user_pass.check_in_time = datetime.now()
    user_pass.save()
    data = {
        'status':True,
        'message':'Successfully checked in!'
    }
    return HttpResponse(json.dumps(data))

@csrf_exempt
@login_required
def scanner(request):
    if request.method == "POST":
        return fetch_user_status(request)
    if request.user.is_staff:
        campus_resources = CampusResource.objects.filter().values('name')
        hostels = Hostel.objects.filter().values('name')
        if request.iOS:
            return render(request, 'info.html', {'campus_resources':campus_resources, 'hostels':hostels})
        else:
            return render(request, 'info.html', {'campus_resources':campus_resources, 'hostels':hostels})
    else:
        return HttpResponse('Invalid Operation')
    


