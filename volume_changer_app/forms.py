from django.forms import ModelForm, ClearableFileInput

from .models import Music

class UploadMusicForm(ModelForm):
    class Meta:
        model = Music
        fields = ('file',)
        labels = {'file': 'Music File'}
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}) 
        }

    def save(self, commit=True):
        """uploadされた複数のfileからMusic instanceを作る"""
        music_list = []
        for f in self.files.getlist('file'):
            music_list.append(Music(file=f, name=f.name))

        if commit:
            for music in music_list:
                music.save()

        return music_list

