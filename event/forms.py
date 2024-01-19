from django import forms
from .models import Event
from taggit.forms import TagWidget

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class CustomTagWidget(TagWidget):
    def __init__(self, attrs=None):
        if attrs is not None:
            attrs['class'] = 'form-control my-2'
        else:
            attrs = {'class': 'form-control my-2'}
        super().__init__(attrs)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class EventCreationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'time', 'location', 'description', 'is_public', 'categories', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'date': forms.DateInput(attrs={'class': 'form-control my-2', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control my-2', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'description': forms.Textarea(attrs={'class': 'form-control my-2'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input my-2'}),
            'categories': forms.Select(attrs={'class': 'form-select my-2'}),
            'tags': CustomTagWidget(),
        }

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
