from django.shortcuts import render

def index(request):
    return render(request, 'volume_changer_app/index.html')
