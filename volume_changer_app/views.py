from django.shortcuts import render, redirect

from .forms import UploadMusicForm

def index(request):
    context = {}
    if request.method == 'POST':
        form = UploadMusicForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vca:download')
    else:
        form = UploadMusicForm()
    context['form'] = form
    return render(request, 'volume_changer_app/index.html', context)

def download(request):
    return render(request, 'volume_changer_app/download.html')
