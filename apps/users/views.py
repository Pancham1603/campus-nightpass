from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views import View
from django.http import HttpResponse
from .models import Student

@csrf_exempt
def login_user(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            registration_id = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=registration_id, password=password)
            if user is not None:
                login(request, user=user)
                request.session['user'] = registration_id
                return redirect('/')
            else:
                messages.error(request, 'Invalid password or account not activated')
                return redirect("/login")
        else:
            return render(request=request, template_name='login.html')
    else:
        return redirect('/events')


def logout_user(request):
    logout(request)
    return redirect('/login')


from faker import Faker
from datetime import date, timedelta
from random import choice
from django.utils import timezone

fake = Faker()

def generate_dummy_student_data():
    data = []
    for _ in range(50):
        student = Student(
            registration_number=fake.unique.random_int(min=101900000, max=102339999),
            name=fake.name(),
            branch=fake.random_element(elements=('Computer Science', 'Electrical Engineering', 'Mechanical Engineering')),
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=25),
            mobile_number=fake.phone_number(),
            father_name=fake.name(),
            mother_name=fake.name(),
            email=fake.email(),
            course=fake.random_element(elements=('B.Tech', 'M.Tech', 'Ph.D.')),
            semester=fake.random_element(elements=('1', '2', '3', '4', '5', '6', '7', '8')),
            parent_contact=fake.phone_number(),
            address=fake.address(),
            qr=fake.url(),
            picture=fake.image_url(),
            room_number=fake.random_element(elements=('101', '102', '201', '202', '301', '302')),
            is_active=True,
            is_staff=False,
            is_superuser=False,
            has_booked=False,
            is_checked_in=True,
            hostel_checkout_time=timezone.now() + timedelta(days=30),
            hostel_checkin_time=timezone.now(),
            last_checkout_time=timezone.now() - timedelta(days=15),
            violation_flags=fake.random_int(min=0, max=5)
        )
        student.set_password('12345678')
        student.save()
        data.append(student)
    return data

# generate_dummy_student_data()