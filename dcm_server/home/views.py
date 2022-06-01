from django.shortcuts import render
from django.http import HttpResponse

from .models import ServerInfo

# Create your views here.


def index(request):
    return HttpResponse("(/) HTTP Response 200!")


def home(request):
    all_servers = ServerInfo.objects.all()
    output = ""
    for s in all_servers:
        output += str(s) + "<br>"
    return HttpResponse(output)
