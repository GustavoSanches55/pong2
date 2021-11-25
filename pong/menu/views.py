from django.shortcuts import render, reverse
from django.http import HttpResponse, Http404
from django.http.response import HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request,"menu/index.html")

def modos(request):
    return render(request,"menu/modos.html")
