from django.db import models
from taggit.managers import TaggableManager
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
# Create your models here.
User = settings.AUTH_USER_MODEL


class PostManager(models.Manager):
    def active(self, *args, **kwargs): # overwriting the default all
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())



def upload_location(instance, filename):
    return ("{0}/{1}").format(instance.id, filename)
    # filebase, extention = filename.splite(".")
    # return "{0}/{1}.{2}".format(instance.id, instance.id, extention)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, default=1)
    title = models.CharField(max_length=33, verbose_name=u'عنوان')
    slug = models.SlugField(unique=True, blank=True, null=False)
    image = models.ImageField(upload_to=upload_location, blank=True, null=True,
                                verbose_name=u'تصویر تور',
                                width_field="width_field",
                                height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField(null=False, blank=True, default='', verbose_name=u'متن')
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=u'آخرین به روزرسانی')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=u'بارگذاری شده')

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})
        # return "/posts/%s/" %(self.id)

    class Meta:
        verbose_name = u'پست'
        verbose_name_plural = u'پست ها'
        ordering = ["-timestamp", "-updated"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = ("{0}-{1}").format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def post_pre_save_signal_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    # slug = slugify(instance.title)
    # exists = Post.objects.filter(slug=slug).exists()
    # if exists:
    #     slug = '{0}-{1}'.format(slug, instance.id)
    # instance.slug = slug

pre_save.connect(post_pre_save_signal_receiver, sender=Post)


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class PublishedBlogManger(models.Manager):
    def get_queryset(self):
        queryset = super(PublishedBlogManger, self).get_queryset().filter(status='published')
        queryset = queryset  # TODO
        return queryset


class Blog(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    category = models.ForeignKey(Category, related_name='category_blog')
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    # status = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    objects = models.Manager()
    published = PublishedBlogManger()

    # query example =>blog.published.filter(title__startswith='Who')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)
        verbose_name = 'post'
        verbose_name_plural = 'Blogs'
