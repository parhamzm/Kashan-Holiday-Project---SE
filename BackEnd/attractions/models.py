from django.db import models

# Create your models here.





# class Attraction(models.Model):
#     name = models.CharField(max_length=120, verbose_name=u'نام مکان', null=False, blank=False, unique=True)
#     introduction = models.TextField(null=False, blank=True, default=u'معرفی')
#     address = models.ForeignKey(Address, on_delete=models.CASCADE)

#     class Meta:
#         pass



class Gallery(models.Model):
    STATUSـCHOICES = (
        ('hotel','Hotel'),
        ('tour','Tour'),
        ('resturant','Resturant'),
        ('location','Location'),
        ('other','Other'),
    )
    name = models.CharField(max_length=250, blank=True, null=True)
    slug = models.SlugField()
    category= models.CharField(max_length=20,choices=STATUSـCHOICES,blank=True, null=True)
    image = models.ImageField(upload_to='gallery')





