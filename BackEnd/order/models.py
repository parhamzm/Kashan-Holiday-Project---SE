from decimal import Decimal
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
# Create your models here.
from cart.models import Cart
import braintree
User = settings.AUTH_USER_MODEL


if settings.DEBUG:
	braintree.Configuration.configure(braintree.Environment.Sandbox,
      merchant_id=settings.BRAINTREE_MERCHANT_ID,
      public_key=settings.BRAINTREE_PUBLIC,
      private_key=settings.BRAINTREE_PRIVATE)



class UserCheckout(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, verbose_name=u"کاربر") #not required
	email = models.EmailField(unique=True, verbose_name=u"ایمیل") #--> required
	braintree_id = models.CharField(max_length=120, null=True, blank=True, verbose_name=u"شماره پرداخت")

	def __str__(self):
		return self.email

	class Meta:
		verbose_name = u'پرداخت'
		verbose_name_plural = u'پرداخت‌ها'

	@property
	def get_braintree_id(self,):
		instance = self
		if not instance.braintree_id:
			result = braintree.Customer.create({
			    "email": instance.email,
			})
			if result.is_success:
				instance.braintree_id = result.customer.id
				instance.save()
		return instance.braintree_id

	def get_client_token(self):
		customer_id = self.get_braintree_id
		if customer_id:
			client_token = braintree.ClientToken.generate({
			    "customer_id": customer_id
			})
			return client_token
		return None


def update_braintree_id(sender, instance, *args, **kwargs):
	if not instance.braintree_id:
		instance.get_braintree_id


post_save.connect(update_braintree_id, sender=UserCheckout)




ADDRESS_TYPE = (
	('billing', 'معرفی'),
	('shipping', 'ارسالی'),
)

class UserAddress(models.Model):
	user = models.ForeignKey(UserCheckout, verbose_name=u"کاربر")
	type = models.CharField(max_length=120, choices=ADDRESS_TYPE, verbose_name=u"نوع آدرس")
	street = models.CharField(max_length=120, verbose_name=u"خیابان")
	city = models.CharField(max_length=120, verbose_name=u"شهر")
	state = models.CharField(max_length=120, verbose_name=u"استان")
	zipcode = models.CharField(max_length=120, verbose_name=u"کد پستی")

	def __str__(self):
		return self.street
	
	class Meta:
		verbose_name = u'آدرس کاربر'
		verbose_name_plural = u'آدرس‌های کاربران'

	def get_address(self):
		return "%s, %s, %s %s" %(self.street, self.city, self.state, self.zipcode)


ORDER_STATUS_CHOICES = (
	('created', 'ایجاد شد'),
	('paid', 'پرداخت شد'),
	('shipped', 'ارسال شد'),
	('refunded', 'بازگشت خورد'),
)


class Order(models.Model):
	status = models.CharField(max_length=120, choices=ORDER_STATUS_CHOICES, default='created', verbose_name=u"وضعیت سفارش")
	cart = models.ForeignKey(Cart, verbose_name=u"سبد خرید")
	user = models.ForeignKey(UserCheckout, null=True, verbose_name=u"کاربر")
	billing_address = models.ForeignKey(UserAddress, related_name='billing_address', null=True, verbose_name=u"آدرس ارسال")
	shipping_address = models.ForeignKey(UserAddress, related_name='shipping_address', null=True, verbose_name=u"آدرس معرفی")
	shipping_total_price = models.DecimalField(max_digits=50, decimal_places=2, default=5.99, verbose_name=u"هزینه‌ها")
	order_total = models.DecimalField(max_digits=50, decimal_places=2, verbose_name=u"مبلغ سفارش")
	order_id = models.CharField(max_length=20, null=True, blank=True, verbose_name=u"شماره سفارش")

	def __str__(self):
		return str(self.cart.id)

	class Meta:
		ordering = ['-id']
		verbose_name = u'سفارش'
		verbose_name_plural = u'سفارشات'

	def get_absolute_url(self):
		return reverse("order_detail", kwargs={"pk": self.pk})

	def mark_completed(self, order_id=None):
		self.status = "paid"
		if order_id and not self.order_id:
			self.order_id = order_id
		self.save()


def order_pre_save(sender, instance, *args, **kwargs):
	shipping_total_price = instance.shipping_total_price
	cart_total = instance.cart.total
	order_total = Decimal(shipping_total_price) + Decimal(cart_total)
	instance.order_total = order_total

pre_save.connect(order_pre_save, sender=Order)

# #if status == "refunded":
# 	braintree refud
# post_save.connect()

# 	