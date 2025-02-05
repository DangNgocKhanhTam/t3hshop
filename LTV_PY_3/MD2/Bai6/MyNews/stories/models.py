from django.db import models
import datetime
from ckeditor_uploader.fields import RichTextUploadingField
class Category(models.Model): 
    name = models.CharField(max_length=150, unique=True)

    def __str__(self): 
        return self.name
    
class Story(models.Model): 
    Category=models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=250,unique=True )
    author = models.CharField(max_length=250)
    url = models.URLField(null=True)
    content = RichTextUploadingField() 
    public_day = models.DateField(default=datetime.date.today)
    image = models.ImageField(upload_to='stories/images', default="stories/images/default_2.jpg")

    def __str__(self): 
        return self.name
    

