from django.db import models
from django.conf import settings
from django.db.models import Q
from .validators import validate_category
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from .utils import unique_slug_generator
from tours.models import Tour
# Create your models here.

User = settings.AUTH_USER_MODEL


class RestaurantLocationQuerySet(models.query.QuerySet):
    def search(self, query): #RestaurantLocation.objects.all().search(query) #RestaurantLocation.objects.filter(something).search()
        if query:
            query = query.strip()
            return self.filter(
                Q(name__icontains=query) |
                Q(location__icontains=query) |
                Q(location__iexact=query) |
                Q(category__icontains=query) |
                Q(category__iexact=query) |
                Q(item__name__icontains=query) |
                Q(item__contents__icontains=query)
                ).distinct()
        return self


class RestaurantLocationManager(models.Manager):
    def get_queryset(self):
        return RestaurantLocationQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


class RestaurantLocation(models.Model):
    owner = models.ForeignKey(User, verbose_name=u'صاحب امتیاز')
    name = models.CharField(max_length=120, verbose_name=u'نام رستوران')
    description = models.TextField(blank=True, verbose_name=u'توضیحات رستوران')
    location = models.CharField(max_length=120, null=True, blank=True, verbose_name=u'مکان')
    image = models.ImageField(upload_to='Hotels/%Y/%m/%d', blank=True)
    category = models.CharField(max_length=120, null=True, blank=True, validators=[validate_category], verbose_name=u'دسته بندی')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=False, blank=True, default='')
    tour = models.ForeignKey(Tour, blank=True, null=True)
    google_map = models.TextField(blank=True,  verbose_name=u"نقشه گوگل", default='<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d462565.197581445!2d54.94755498654818!3d25.075085310621688!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3e5f43496ad9c645%3A0xbde66e5084295162!2sDubai+-+United+Arab+Emirates!5e0!3m2!1sen!2s!4v1531633872589" width="600" height="450" frameborder="0" style="border:0" allowfullscreen></iframe>')

    def __str__(self):
        return self.name

    objects = RestaurantLocationManager()

    def get_absolute_url(self):
        # return f"/restaurants/{self.slug}"
        return reverse('restaurants:rest_detail', kwargs={'slug': self.slug})

    


    @property
    def title(self):
        return self.name

    class Meta:
        verbose_name = u'رستوران'
        verbose_name_plural = u'رستوران ها'


def restaurant_location_pre_save_receiver(sender, instance, *args, **kwargs): # before save
    print('Saving ...')
    instance.category = instance.category.capitalize()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


# def restaurant_location_post_save_receiver(sender, instance, created, *args, **kwargs): # after save
#     print('saved')
    # if not instance.slug:
    #     instance.slug = unique_slug_generator(instance)
    #     instance.save()

pre_save.connect(restaurant_location_pre_save_receiver, sender=RestaurantLocation)
# post_save.connect(restaurant_location_post_save_receiver, sender=RestaurantLocation)


# class Item(models.Model):
#     user = models.ForeignKey(User)
#     restaurant = models.ForeignKey(RestaurantLocation, on_delete=models.PROTECT)
#     name = models.CharField(max_length=120)
#     contents = models.TextField(help_text='separate each item by comma!')
#     excludes = models.TextField(blank=True, null=True, help_text='separate each item by comma!')
#     public = models.BooleanField(default=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ['-updated', '-timestamp']
#
#     def get_contents(self):
#         return self.contents.split(",")
#
#     def get_excludes(self):
#         return self.excludes.split(",")
