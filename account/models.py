from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Account(AbstractUser):
    user_role = models.CharField(max_length=20, choices=[('organizer', 'Event Organizer'), ('attendee', 'Attendee')])
