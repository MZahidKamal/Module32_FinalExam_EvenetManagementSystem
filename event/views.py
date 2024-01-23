from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import EventCreationForm
from .models import Event, Attendee, EventCategory

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Create your views here.
def all_event_list(request):
    category_list = EventCategory.objects.all()
    category_filter = request.GET.get('category')
    if category_filter:
        events = Event.objects.filter(is_public=True, categories__name=category_filter)
        # return render(request, 'event/event_list.html', {'events': events, 'category_list': category_list})
        return render(request, 'index.html', {'events': events, 'category_list': category_list})
    tag = request.GET.get("tag")
    if tag:
        events = Event.objects.filter(is_public=True, tags__name__in=[tag])
        # return render(request, 'event/event_list.html', {'events': events, 'category_list': category_list})
        return render(request, 'index.html', {'events': events, 'category_list': category_list})
    events = Event.objects.filter(is_public=True)
    # return render(request, 'event/event_list.html', {'events': events, 'category_list': category_list})
    return render(request, 'index.html', {'events': events, 'category_list': category_list})

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    attendees = event.attendees.all()
    return render(request, 'event/event_detail.html', {'event': event, 'attendees': attendees})

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@login_required
def create_event(request):
    form = EventCreationForm()
    if request.user.user_role == 'organizer':
        if request.method == 'POST':
            form = EventCreationForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.organizer = request.user
                event.save()
                form.save_m2m()  # Save many-to-many fields
                return redirect('my_event_details', id=event.id)  # Redirect to the event detail page
        else:
            form = EventCreationForm()
    else:
        # messages.error(request, "Document deleted.")
        return redirect('event')
    return render(request, 'event/create_event.html', {'form': form})

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@login_required
def add_attendee(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    print(event_id)
    # Check if the user is not the organizer and is not already attending
    if request.user.user_role == 'attendee' and request.user not in event.attendees.all():
        event.attendees.add(request.user)
        event.save()
        Attendee.objects.create(user=request.user, event=event)
        return redirect('event_detail', event_id=event.id)
    else:
        return JsonResponse({'message': 'Your account is an organizer account'})
    # attendees_list = list(event.attendees.values('username'))
    return redirect('event_detail', event_id=event.id)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def accept_attendees(request, id):
    attendee = Attendee.objects.get(id=id)
    attendee.accepted = True
    attendee.save()
    return redirect('my_event_details', id=attendee.event.id)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Organizer Dashboard
def my_event(request):
    if request.user.user_role == 'organizer':
        event_list = Event.objects.filter(organizer=request.user)
        return render(request, 'event/my_event_list.html', {'event_list': event_list})
    else:
        return redirect('event')

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def my_event_details(request, id):
    if request.user.user_role == 'organizer':
        event = Event.objects.get(organizer=request.user, id=id)
        attendees = Attendee.objects.filter(event=event)
        return render(request, 'event/my_event_details.html', {'event': event, 'attendees': attendees})

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def delete_event(request, id):
    event = Event.objects.get(id=id)
    event.delete()
    return redirect('my_event')

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def update_event(request, id):
    form = EventCreationForm()
    event = Event.objects.get(id=id)

    if request.method == 'POST':
        form = EventCreationForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            form.save_m2m()  # Save many-to-many fields
            return redirect('my_event_details', id=event.id)  # Redirect to the event detail page
    else:
        form = EventCreationForm(instance=event)

    return render(request, 'event/update_event.html', {'form': form})

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Attendees Dashboard
def my_attendees(request):
    user = request.user
    accepted_filter = request.GET.get('accepted')
    if accepted_filter == 'true':
        events_attending = Attendee.objects.filter(user=user, accepted=True)
        return render(request, 'event/my_attendees.html', {'events_attending': events_attending})
    if accepted_filter == 'false':
        events_attending = Attendee.objects.filter(user=user, accepted=False)
        return render(request, 'event/my_attendees.html', {'events_attending': events_attending})

    events_attending = Attendee.objects.filter(user=user)
    return render(request, 'event/my_attendees.html', {'events_attending': events_attending})

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
