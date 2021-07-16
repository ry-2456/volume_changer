import logging
import mimetypes
import shutil
import urllib.parse

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UploadMusicForm
from .models import Music

def index(request):
    context = {}
    if request.method == 'POST':
        form = UploadMusicForm(request.POST, request.FILES)
        if form.is_valid():
            music_list = form.save()
            request.session['uploaded_music_pk_list'] = [m.pk for m in music_list]
            return redirect('vca:download_list')
    else:
        form = UploadMusicForm()
    context['form'] = form
    return render(request, 'volume_changer_app/index.html', context)

def download(request, pk):
    """clickでdownloadを実行"""
    uploaded_music = get_object_or_404(Music, pk=pk) 
    filename = uploaded_music.name
    guessed_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(content_type=guessed_type or 'application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename={urllib.parse.quote(filename)}' # force download
    shutil.copyfileobj(uploaded_music.file, response) # copy file to response
    return response

def download_list(request):
    """downloadできるfileのlist"""
    # server側でdonwload機能を実装するのがいいのか?
    context = {}
    uploaded_music_pk_list = request.session.get('uploaded_music_pk_list')
    if uploaded_music_pk_list:
        uploaded_music_list = [Music.objects.get(pk=pk) for pk in uploaded_music_pk_list]
        context['uploaded_music_list'] = uploaded_music_list
    return render(request, 'volume_changer_app/download_list.html', context)
