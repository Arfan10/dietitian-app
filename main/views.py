from django.shortcuts import render,redirect
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from .models import Appointment, Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from .token import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str



def home(request):
    return render(request, 'main/home.html')


@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user=request.user
            appointment.save()
            subject = "Your Appointment Confirmation"
            message =(
                f"Hello {appointment.full_name},\n\n"
                f"Your appointment has been booked successfully! \n\n"
                f"Date:{appointment.date}\n"
                f"Time: {appointment.time}\n\n"
                f"Thankyou for choosing our services.\n"
            )
            recipient = [appointment.email]
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient,
                fail_silently = False
            )
            return redirect('Success_Appointment')
        else:
            print("Form is not valid!")
            print(form.errors)
    else:
        form = AppointmentForm()

    return render(request,'main/book_appointment.html',{'form':form})

def appointment_success(request):
    return render(request, 'main/success.html') 

def signup_view(request):
    if request.method =="POST":
        username= request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST.get('role','User')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request,'username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request,'Email already exists')
            else:
                user= User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user.profile.role = role
                user.profile.save()
                messages.success(request, 'Account Created Successfully! Please Login.')
                return redirect('login')
        else:
            messages.error(request,'password do not match')
    return render(request, 'main/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password= request.POST['password']

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            #role-base redirect
            if hasattr(user,'profile') and user.profile.role == 'Dietitian':
                return redirect('dietitian_dashboard')
            else:
                return redirect('home')
    else:
            messages.error(request,"Invalid Username or Password")
    return render(request,'main/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def success_page(request):
    return redirect(request, 'success.html')


@login_required
def user_dashboard(request):
    user_appointments = Appointment.objects.filter(user = request.user).order_by('-date')
    return render(request,'main/user_dashboard.html',{'appointments':user_appointments})

@login_required
def user_appointments(request):
   appointments = Appointment.objects.filter(user=request.user).order_by('-date')
   return render(request, 'main/user_appointments.html', {'appointments': appointments})

@login_required
def dietitian_dashboard(request):
    if hasattr(request.user, 'profile') and request.user.profile.role == 'Dietitian':
        appointment = Appointment.objects.all().order_by('-date','time')
        return render(request, 'main/dietitian_dashboard.html',{'appointment':appointment})
    else:
        return redirect('user_dashboard')

