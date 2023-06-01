from django import forms
from room.models import *

class CreateRoomForm(forms.ModelForm):

    room_name = forms.CharField(label='Room name', required=True, max_length=200, min_length=5)
    name = forms.CharField(label='Your name', required=True, max_length=50, min_length=5)

    class Meta:
        model = User
        fields = ('name',)