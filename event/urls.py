from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_event_list, name='home'),
    path('', views.all_event_list, name='event'),
    path('event/under_development', views.under_development, name='under_development'),
    path('create-event/', views.create_event, name='create_event'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('add_attendee/<int:event_id>/', views.add_attendee, name='add_attendee'),
    path('my-event/', views.my_event, name='my_event'),
    path('my-event-details/<int:id>/', views.my_event_details, name="my_event_details"),
    path('delete-event/<int:id>/', views.delete_event),
    path('update-event/<int:id>/', views.update_event),
    path('attendees/', views.my_attendees),
    path('accept/<int:id>/', views.accept_attendees),
]