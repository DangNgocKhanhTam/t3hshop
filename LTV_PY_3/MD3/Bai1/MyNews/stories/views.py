from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.
now = datetime.datetime.now()

def index(request): 
    return render(request,'stories/index.html', {'today':now})


def category(request): 
    return render(request, 'stories/category.html',  {'today':now})

def story(request): 
    return render(request, 'stories/story.html', {'today':now})

def contact(request): 
    return render(request, 'stories/contact.html', {'today':now})

def detail(request): 
    return HttpResponse(request, "hello")