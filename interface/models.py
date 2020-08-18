from django.db import models
import random 

def shorten_code_generator(size = 6):
    chars = 'abcdefghijklmopqrstuvvwxyzABCDEFGHIJKLIMNOPQRSTUVWXYZ'

    currcode = ''.join(random.choice(chars) for i in range(size))

    if shorturl.objects.filter(shortened = currcode).exists():
        return shorten_code_generator()

    return currcode

class ShortURLManager(models.Manager):
    def all(self,*args,**kwargs):

        main = super(ShortURLManager,self).all(*args,**kwargs).filter(active=False)

        return main
    
    def refresh(self):

        main = shorturl.objects.filter(id__gte = 1)

        for URLObject in main:
            URLObject.shortened = shorten_code_generator()
            print(URLObject)
            URLObject.save()
        

# Create your models here.
class shorturl(models.Model):

    url = models.CharField(max_length=300,)
    shortened = models.CharField(max_length = 20,unique = True,null = False,blank = True)
    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add = True)
    active = models.BooleanField(default = True)
    clicks_total = models.IntegerField(default=0)
    clicks_average = models.IntegerField(default=0)
    user = models.CharField(max_length = 100)

    objects = ShortURLManager()

    def save(self, *args, **kwargs):
        if self.shortened is None or self.shortened == "":
            self.shortened = shorten_code_generator()
            
        super(shorturl, self).save(*args,**kwargs)

    def __str__(self):
        return str(self.url)
    
    def __unicode__(self):
        return str(self.url)
    