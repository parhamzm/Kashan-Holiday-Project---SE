from django.db import models
from accounts.models import UserAddresses
from django.urls import reverse
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
# from restaurants.models import RestaurantLocation
# Create your models here.


class TourQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class AvailableTourManger(models.Manager):
    def get_queryset(self):
        return TourQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()
        # queryset = super(AvailableTourManger, self).get_queryset().filter(available=True)
        # queryset = queryset  # TODO
        # return queryset


class Tour(models.Model):
    name = models.CharField(max_length=250, db_index=True, verbose_name=u'نام تور')
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to='Tour/%Y/%m/%d', blank=True, verbose_name=u"تصویر")
    description = models.TextField(blank=True, verbose_name=u'توضیحات تور')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'قیمت تور')
    available = models.BooleanField(default=True, verbose_name=u'موجود بودن')
    categories = models.ManyToManyField('TourCategory', blank=True)
    default = models.ForeignKey('TourCategory', related_name='default_category', null=True, blank=True, verbose_name=u'دسته‌بندی پیش‌فرض')
    start_tour = models.DateTimeField(blank=True, null=True, verbose_name=u"زمان شروع تور")
    end_tour = models.DateTimeField(blank=True, null=True, verbose_name=u"زمان پایان تور")
    created = models.DateTimeField(auto_now_add=True, verbose_name=u"تاریخ ایجاد")
    updated = models.DateTimeField(auto_now=True, verbose_name=u"به‌روزرسانی شده در")
    active = models.BooleanField(default=True, blank=True, verbose_name=u'فعال')
    note = models.TextField(blank=True, verbose_name=u'نکات تور')
    # restaurant = models.ManyToManyField(RestaurantLocation)

    objects = AvailableTourManger()
    published = AvailableTourManger()

    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)
        verbose_name = u'تور'
        verbose_name_plural = u'تورها'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse('Tour_Detail', kwargs={"pk":self.pk, "slug":self.slug})
        # args=[self.pk, self.slug],
        return reverse('tours:Tour_Detail', kwargs={"pk":self.pk, "slug":self.slug})


class TourVariation(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.PROTECT)
    title = models.CharField(max_length=120, verbose_name=u'نام')
    price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    active = models.BooleanField(default=True)
    inventory = models.PositiveIntegerField(null=True, blank=True)  # unlimited

    def __str__(self):
        return self.title

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    def get_absolute_url(self):
        return self.tour.get_absolute_url()

    def add_to_cart(self):
        return "%s?item=%s&qty=1" % (reverse("cart"), self.id)

    def remove_from_cart(self):
        return "%s?item=%s&qty=1&delete=True" % (reverse("cart"), self.id)

    def get_title(self):
        return "%s - %s" % (self.tour.name, self.title)


def tour_post_save_receiver(sender, instance, created, *args, **kwargs):
    tour = instance
    variations = tour.tourvariation_set.all()
    if variations.count() == 0:
        new_var = TourVariation()
        new_var.tour = tour
        new_var.title = "Default"
        new_var.price = tour.price
        new_var.save()


post_save.connect(tour_post_save_receiver, sender=Tour)


def image_upload_to(instance, filename):
    title = instance.tour.name
    slug = slugify(title)
    file_extension = filename.split(".")[1]
    new_filename = "{0}-{1}.{2}".format(slug, instance.id, file_extension)
    return "tours/{0}/{1}".format(slug, new_filename)


class TourImage(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.PROTECT)
    image = models.ImageField(upload_to=image_upload_to)

    class Meta:
        verbose_name = u'تصویر'
        verbose_name_plural = u'تصاویر'

    def __str__(self):
        return self.tour.name


class TourCategory(models.Model):
    title = models.CharField(max_length=120, unique=True, verbose_name=u"نام دسته")
    slug = models.SlugField(unique=True)
    description = models.TextField(null=False, blank=True, default='', verbose_name=u'توضیحات')
    active = models.BooleanField(default=True, verbose_name=u'فعال')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name = u'دسته‌بندی'
        verbose_name_plural = u'دسته‌بندی‌ها'

    def __str__(self):
        return self.title

    def get_absolute_url(self, *args, **kwargs):
        return reverse("category_detail", kwargs={"slug": self.slug})


def image_upload_to_featured(instance, filename):
    title = instance.tour.name
    slug = slugify(title)
    file_extension = filename.split(".")[1]
    new_filename = "{0}-{1}.{2}".format(slug, instance.id, file_extension)
    return "tours/{0}/featured/{1}".format(slug, new_filename)


class TourFeatured(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.PROTECT, verbose_name=u"نام تور")
    image = models.ImageField(upload_to=image_upload_to_featured, verbose_name=u"تصویر")
    title = models.CharField(max_length=120, null=True, blank=True, verbose_name=u"عنوان")
    text = models.CharField(max_length=220, null=True, blank=True, verbose_name=u"متن")
    text_right = models.BooleanField(default=False, verbose_name=u"راست‌چین")
    show_price = models.BooleanField(default=False, verbose_name=u"نمایش قیمت")
    active = models.BooleanField(default=True, verbose_name=u"فعال")

    def __str__(self):
        return self.tour.name

    
