from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, pre_save
# Create your models here.

User = settings.AUTH_USER_MODEL


class AvailableTourManger(models.Manager):
    def get_queryset(self):
        queryset = super(AvailableTourManger, self).get_queryset().filter(available=True)
        queryset = queryset  # TODO
        return queryset

class Hotel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=120, verbose_name=u'نام هتل', null=False, blank=True)
    description = models.TextField(blank=True, verbose_name=u'توضیحات رستوران')
    slug = models.SlugField(null=False, blank=True, unique=True)
    image = models.ImageField(upload_to='Hotels/%Y/%m/%d', blank=True, verbose_name=u"تصویر")
    description = models.TextField(null=False, blank=True, default='Welcome to our city !!!')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=u"تاریخ ایجاد")
    available = models.BooleanField(default=True, verbose_name=u"موجود بودن")

    objects = models.Manager()
    published = AvailableTourManger()


    def get_absolute_url(self):
        # return f"/restaurants/{self.slug}"
        return reverse('hotel:hotel_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = u"هتل"
        verbose_name_plural = u"هتل ها"


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT)
    typeName = models.CharField(max_length=120, verbose_name=u'نام نوع اتاق', null=False, blank=True)
    capacity = models.PositiveSmallIntegerField(verbose_name=u'ظرفیت اتاق', null=True, blank=True, default=2)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.typeName

    def get_absolute_url(self):
        return reverse("room_type", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = u'نوع اتاق'
        verbose_name_plural = u'انواع اتاق'


class HotelRoom(models.Model):
    host = models.ForeignKey(User, on_delete=models.PROTECT)
    roomType = models.ForeignKey(RoomType, on_delete=models.PROTECT)
    roomNumber = models.PositiveIntegerField(verbose_name=u'شماره اتاق', null=False, blank=False, default=100)
    price = models.DecimalField(decimal_places=2, max_digits=20, default=99.99)
    sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    inventory = models.IntegerField(verbose_name=u"موجودی", null=True, blank=True)

    def __str__(self):
        return self.roomNumber
    
    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    def get_absolute_url(self):
        return self.roomType.get_absolute_url()



def product_saved_receiver(sender, instance, *args, **kwargs):
    print(sender)
    roomtype = instance
    variations = roomtype.hotelroom_set.all()
    if variations.count() == 0:
        new_var = HotelRoom()
        new_var.roomType = roomtype
        new_var.roomNumber = "123"
        new_var.price = roomtype.price
        new_var.save()
    # variations = HotelRoom.objects.filter(roomtype=roomtype)

post_save.connect(product_saved_receiver, sender=RoomType)
