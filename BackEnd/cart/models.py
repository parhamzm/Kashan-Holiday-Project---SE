from django.db import models
from django.conf import settings
from decimal import Decimal
from tours.models import Tour, TourVariation
from accounts.models import BasicUser
from django.db.models.signals import pre_save, post_save, post_delete
from django.core.urlresolvers import reverse
# Create your models here.
User = settings.AUTH_USER_MODEL


class CartItemHotel(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.PROTECT, verbose_name=u"سبد خرید")
    # item = models.ForeignKey("", verbose_name=u"")
    quantity = models.PositiveIntegerField(default=1, verbose_name=u"تعداد")


class CartItem(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.PROTECT, verbose_name=u"سبد خرید")
    item = models.ForeignKey(TourVariation, on_delete=models.PROTECT, verbose_name=u"مورد")
    quantity = models.PositiveIntegerField(default=1, verbose_name=u"تعداد")
    line_item_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u"قیمت")

    def __str__(self):
        return self.item.title

    def remove(self):
        return self.item.remove_from_cart()


def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = instance.quantity
    if int(qty) >= 1:
        price = instance.item.get_price()
        line_item_total = Decimal(qty) * Decimal(price)
        instance.line_item_total = line_item_total


pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)


def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.update_subtotal()


post_save.connect(cart_item_post_save_receiver, sender=CartItem)
post_delete.connect(cart_item_post_save_receiver, sender=CartItem)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, verbose_name=u"کاربر")
    items = models.ManyToManyField(TourVariation, through=CartItem, verbose_name=u"محتویات")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=u"زمانن ایجاد")
    updated = models.DateTimeField(auto_now=True, verbose_name=u"به‌روزرسانی شده در")
    subtotal = models.DecimalField(max_digits=50, default=100.00, verbose_name=u'مجموع', decimal_places=2)
    tax_total = models.DecimalField(max_digits=50, default=100.00, verbose_name=u'مجموع مالیات', decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=10, decimal_places=5, default=0.01, verbose_name=u'درصد مالیات')
    total = models.DecimalField(max_digits=50, default=100.00, verbose_name=u'جمع کل', decimal_places=2)
    # discounts

    class Meta:
        verbose_name = u'سبد خرید'
        verbose_name_plural = u'سبدهای خرید'

    def __str__(self):
        return str(self.id)

    def update_subtotal(self):
        print("Updating...")
        subtotal = 0
        items = self.cartitem_set.all()
        for item in items:
            subtotal += item.line_item_total
        self.subtotal = "%.2f" % (subtotal)
        self.save()


def calculate_tax_total_price_receiver(sender, instance, *args, **kwargs):
    subtotal = Decimal(instance.subtotal)
    tax_total = round(subtotal * Decimal(instance.tax_percentage), 2) # ده درصد مالیات برارزش افزوده
    total = round(subtotal + Decimal(tax_total), 2)
    instance.tax_total = "%.2f" %(tax_total)
    instance.total = "%.2f" %(total)


pre_save.connect(calculate_tax_total_price_receiver, sender=Cart)

