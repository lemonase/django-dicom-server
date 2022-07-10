from django.shortcuts import render
from django.http import HttpResponse

from .models import DicomServer

# Create your views here.


def index(request):
    all_servers = DicomServer.objects.all()

    server_list = {'server_list': all_servers}
    return render(request, 'home/index.html', server_list)
