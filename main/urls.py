from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view,name="login"),
    path("logout/", views.logout_view, name="Logout"),
    path('book/', views.book_appointment, name='book_appointment'),
    path('success/', views.appointment_success, name='Success_Appointment'),
    path('appointments/', views.user_appointments, name='user_appointments'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('dietitian/dashboard/', views.dietitian_dashboard, name='dietitian_dashboard'),



]