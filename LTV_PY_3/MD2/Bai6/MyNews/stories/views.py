import datetime
from django.shortcuts import render
from . import models
import re
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.
from django.http import HttpResponse

now = datetime.datetime.now()
def index(request):

    story_list= models.Story.objects.order_by("-public_day")
    newest = story_list[0]
    next_4_newest = story_list[1:5]
    young_children = models.Story.objects.filter(Category_id=1 ).order_by('-public_day')
    older_children = models.Story.objects.filter(Category_id = 2).order_by('-public_day')

    return render(request, "stories/index.html", 
                  {'today':now, 'stories':story_list, 
                   'newest':newest,
                   'next_4_stories': next_4_newest,
                   'young': young_children, 
                   'older': older_children
                   }
                  )
    #return HttpResponse("Hello and welcome to <b>Stories for Children</b> app!")
    
    # return render(request, "stories/index.html", {'today':now})

def category(request, pk):
    story_list = models.Story.objects.filter(Category_id=pk)
    for story in story_list: 
        story.content = re.sub('<[^<]+?>', '', story.content)

    page = request.GET.get('page', 1)
    paginator = paginator(story_list,4)

    try: 
        stories = paginator.page(page)
    except PageNotAnInteger:
        stories = paginator.page(1)
    except EmptyPage:
        stories = paginator.page(paginator.num_pages)



    newest = models.Story.objects.filter(Category_id=pk).order_by('-public_day')[0:4]
    
    return render(request,"stories/category.html",
                  {'today': now,
                   'stories':story_list,
                   'newest': newest,
                   'pk':pk})


def story(request, a):
    story_select = models.Story.objects.get(pk=a)
    stories = models.Story.objects.filter(Category_id=story_select.Category_id).order_by('-public_day')
    newest = models.Story.objects.order_by('-public_day')[:4]
    return render(request, "stories/story.html", {
        'today': now, 
        'story': story_select, 
        'stories': stories,
        'newest': newest
    })



def contact(request):
    return render(request, "stories/contact.html", {'today':now})
    
