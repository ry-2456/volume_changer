from django import forms

from .models import Music

class UploadMusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ('file',)
        labels = {'file': 'Music File'}
