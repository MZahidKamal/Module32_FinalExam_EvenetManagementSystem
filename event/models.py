from account.models import Account
from django.db import models
from taggit.managers import TaggableManager

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class EventCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Event(models.Model):
    organizer = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    is_public = models.BooleanField(default=True)
    categories = models.ForeignKey(EventCategory, on_delete=models.CASCADE, blank=True, null=True)
    tags = TaggableManager()
    attendees = models.ManyToManyField(Account, related_name='events_attending', blank=True)

    def __str__(self):
        return self.name

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Attendee(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, default=None)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None)
    accepted = models.BooleanField(default=False)
