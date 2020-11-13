from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
	name = models.CharField(max_length=200,null=True)
	email = models.CharField(max_length=200,null=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	CATEGORY = (
		('MenFashion','MenFashion'),
		('WomenFashion','WomenFashion'),
		('KidsFashion','KidsFashion'),
		('Watches','Watches'),
		('Shoes','Shoes'),
	)
	product_name = models.CharField(max_length=264,null=True)
	category = models.CharField(max_length=264,blank=True,choices=CATEGORY) 
	price = models.FloatField()
	image = models.URLField(blank=False)
	description = models.TextField(max_length=500)
	digital = models.BooleanField(default=False,null=True,blank=False)

	def __str__(self):
		return self.product_name


class Order(models.Model):
	customer = models.ForeignKey(Customer,null=True,blank=True,on_delete=models.SET_NULL)
	date_orderd = models.DateTimeField(auto_now_add =True,null=True,blank=True)
	transaction_id = models.CharField(max_length = 200,null=True)
	complete = models.BooleanField(default=False,blank=False,null=True)

	def __str__(self):
		return str(self.id)

	@property
	def get_cart_total(self):
		items = self.orderitem_set.all()
		total = sum([item.get_total for item in items])
		return total

	@property
	def get_cart_items(self):
		items = self.orderitem_set.all()
		total = sum([item.quantity for item in items])
		return total
	


class OrderItem(models.Model):
	order = models.ForeignKey(Order,null=True,blank=True,on_delete=models.SET_NULL)
	product = models.ForeignKey(Product,null=True,blank=True,on_delete=models.SET_NULL)
	date_added = models.DateTimeField(auto_now_add =True,null=True)
	quantity = models.PositiveIntegerField(default=0,null=True,blank=True)

	def __str__(self):
		return self.product.product_name


	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total
	

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer,null=True,blank=True,on_delete=models.SET_NULL)
	product = models.ForeignKey(Product,null=True,blank=True,on_delete=models.SET_NULL)
	address = models.CharField(max_length=264,null=True)
	city = models.CharField(max_length=264,null=True)
	pincode = models.CharField(max_length=264,null=True)
	state = models.CharField(max_length=264,null=True)
	date_added = models.DateTimeField(auto_now_add =True)

	def __str__(self):
		return self.customer.name