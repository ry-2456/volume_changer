import logging
import mimetypes
import shutil
import urllib.parse
from pathlib import Path

import audiofile
import soundfile as sf
import pyloudnorm as pyln

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

from .forms import UploadMusicForm
from .models import Music
from .settings import TARGET_LOUDNESS, SAVE_TO

# TODO: 音が劣化しないようにファイル形式変更方法を工夫
def index(request):
    context = {}
    if request.method == 'POST':
        form = UploadMusicForm(request.POST, request.FILES)
        if form.is_valid():
            music_list = form.save()

            # loudness normalization
            for m in music_list:
                # 音源データ読み込み
                src_path = Path(m.file.path)
                data, sampling_rate = audiofile.read(m.file.path, always_2d=True)

                # loudness計測
                meter = pyln.Meter(sampling_rate)
                current_loudness = meter.integrated_loudness(data.T)

                # loudness normalization
                loudness_normalized_audio = \
                    pyln.normalize.loudness(data.T, current_loudness, TARGET_LOUDNESS)
                normalized_loudness = meter.integrated_loudness(loudness_normalized_audio)

                # save loudness normalized audio
                # save_path : /abosolute/path/to/audiofile.ext
                save_path = src_path.parent.parent / SAVE_TO / src_path.name
                if not save_path.parent.exists():
                    save_path.parent.mkdir()

                # .wavとして保存 (audiofile(soundfile)がwav,flac,oggのみをサポート)
                audiofile.write(
                    save_path.with_suffix('.wav'), 
                    loudness_normalized_audio.T, 
                    sampling_rate
                )

                # TODO: 元々のファイル形式に変換

            # redirectではcontextが渡せないのでsessionで渡す
            request.session['uploaded_music_pk_list'] = [m.pk for m in music_list]
            return redirect('vca:index')
    else:
        form = UploadMusicForm()
    context['form'] = form

    # musicのdownload list
    uploaded_music_pk_list = request.session.get('uploaded_music_pk_list')
    if uploaded_music_pk_list:
        uploaded_music_list = [Music.objects.get(pk=pk) for pk in uploaded_music_pk_list] 
        context['uploaded_music_list'] = uploaded_music_list

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

