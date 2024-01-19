from django.contrib import admin
from .models import Event, EventCategory, Attendee

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    pass
