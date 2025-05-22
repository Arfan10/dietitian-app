from django.db import models
from django.contrib.auth.models import User 

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(blank = True)

    def __str__(self):
        return f"Appointment for {self.full_name} on {self.date} at {self.time}"
    
class Dietplan(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to="diet_plans/") # For downloading file 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('dietitian', 'Dietitian'),
    )
    user= models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
    is_dietitian = models.BooleanField(default=False)
    role= models.CharField(max_length=10,choices = ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
    

class Client(models.Model):
    dietitian = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})"
