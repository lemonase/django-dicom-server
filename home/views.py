from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.http import HttpResponse

from .models import DicomServer

# Create your views here.


class DicomServerListView(ListView):
    model = DicomServer
    context_object_name = 'server_list'


class DicomServerDetailView(DetailView):
    model = DicomServer
    queryset = DicomServer.objects.all()
    context_object_name = 'server'


def index(request):
    all_servers = DicomServer.objects.all()

    server_list = {'server_list': all_servers}
    return render(request, 'home/index.html', server_list)
