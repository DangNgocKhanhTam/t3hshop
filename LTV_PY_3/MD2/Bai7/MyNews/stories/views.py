import datetime
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

now = datetime.datetime.now()
def index(request):
    #return HttpResponse("Hello and welcome to <b>Stories for Children</b> app!")
    
    return render(request, "stories/index.html", {'today':now})

def category(request):
    return render(request, "stories/category.html", {'today':now})

def story(request):
    return render(request, "stories/story.html", {'today':now})

def contact(request):
    return render(request, "stories/contact.html", {'today':now})
    
