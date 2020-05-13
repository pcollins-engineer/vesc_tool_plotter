from django import forms
from django.forms import ModelForm
from . import models

class FoilForm(ModelForm):
    class Meta:
        model = models.Foil
        fields = ['title', 'description']

class BoardForm(ModelForm):
    class Meta:
        model = models.Board
        fields = ['title', 'description']

class MotorForm(ModelForm):
    class Meta:
        model = models.Motor
        fields = ['title', 'description']

class PropellerForm(ModelForm):
    class Meta:
        model = models.Propeller
        fields = ['title', 'description']

class ControllerForm(ModelForm):
    class Meta:
        model = models.Controller
        fields = ['title', 'description']

class RideForm(ModelForm):
    class Meta:
        model = models.Ride
        fields = ['title', 'description', 'ride_date', 'location', 'file']

class BuildForm(ModelForm):
    class Meta:
        model = models.Build
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e-Foil 1.0'}),
            'description': forms.Textarea(
                attrs={'placeholder': 'Enter description here'}),
        }
