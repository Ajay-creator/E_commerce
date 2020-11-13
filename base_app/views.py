from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from .forms import CreateUserForm,AddressForm
from .models import *
# Create your views here.

def home(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		cartItems = order.get_cart_items

	else:
		cartItems = 0

	context = {"cartItems":cartItems,}
	return render(request,"base_app/home.html",context)


def SignupPage(request):
	if request.user.is_authenticated:
		return redirect("home")

	else:	
		form = CreateUserForm()
		if request.method =="POST":
			form = CreateUserForm(request.POST)
			if User.objects.filter(username=request.POST.get("username")).exists() and User.objects.filter(email=request.POST.get("email")).exists():
				messages.info(request,"You have already been registered! Please,login with your credentials")
			elif User.objects.filter(username=request.POST.get("username")).exists():
				messages.warning(request,"The given username is already in use.Please,choose another one ")

			elif User.objects.filter(email=request.POST.get("email")).exists():
				messages.warning(request,"The given email is already registered")

			else:

				if form.is_valid():
					user = form.save()

					customer=Customer.objects.create(user=user)
					username = form.cleaned_data.get("username")
					messages.success(request,"Account has been successfully created for "+username)
					return redirect("login")

				else:
					messages.error(request,"Password must be atleast 8 characters long and should cantain letters, numbers and speacial characters")

	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		cartItems = order.get_cart_items

	else:
		cartItems = 0

	context = {"cartItems":cartItems,"form":form}
	return render(request,"base_app/signup.html",context)

def LoginPage(request):
	if request.user.is_authenticated:
		return redirect("home")

	else:
		if request.method == "POST":
			username = request.POST.get("username")
			password = request.POST.get("password")
			user_auth = authenticate(request,username=username,password=password)
			print(user_auth)
			if user_auth is not None:
				login(request,user_auth)
				context={}
				return render(request,'base_app/home.html',context)
			else:
				messages.error(request,"Username or Password is incorrect")

	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		cartItems = order.get_cart_items

	else:
		cartItems = 0

	context = {"cartItems":cartItems,}	
	return render(request,"base_app/login.html",context)

@login_required
def LogoutUser(request):
	logout(request)
	return redirect("home")


def MensFashionPage(request):
	products = Product.objects.filter(category="MenFashion")

	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		cartItems = order.get_cart_items

	else:
		cartItems = 0

	context = {"cartItems":cartItems,"products":products}

	return render(request,"base_app/men_fashion.html",context)

def WomensFashionPage(request):
	products = Product.objects.filter(category="WomenFashion")

	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		cartItems = order.get_cart_items

	else:
		cartItems = 0

	context = {"cartItems":cartItems,"products":products}

	return render(request,"base_app/women_fashion.html",context)

def OrderPage(request):
	
	form = OrderForm()
	if request.method=="POST":
		form = OrderForm(request.POST)
		if form.is_valid:
			order=form.save()

		else:
			return redirect("order")

	context = {"form":form}
	return render(request,"base_app/order.html",context)


def Cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		if(len(items)>0):
			msg = "Want to add more into cart ? Go ahead!"
		else:
			msg = "What are you looking ? Grab something and fill your cart."
	else:
		items=[]
		order = {"get_cart_total":0,"get_cart_items":0}
		msg = "Please login to fill your cart.😀"

	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		cartItems = order.get_cart_items

	else:
		cartItems = 0


	context={"items":items,"order":order,"msg":msg,"cartItems":cartItems}
	return render(request,"base_app/cart.html",context)


def UpdateItem(request):
	data = json.loads(request.body)
	productId = data["productId"]
	action = data["action"]

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order,created = Order.objects.get_or_create(customer = customer,complete=False)
	orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)

	if action=="add":
		orderItem.quantity= orderItem.quantity + 1
	if action=="remove":
		orderItem.quantity= orderItem.quantity - 1

	orderItem.save()

	if orderItem.quantity<=0:
		orderItem.delete()

	return JsonResponse("Item was added to cart",safe=False)

@login_required
def Checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
	else:
		items=[]
		order = {"get_cart_total":0,"get_cart_items":0}
	form = AddressForm

	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		cartItems = order.get_cart_items

	else:
		cartItems = 0

	context={"form":form,"order":order,"items":items,"cartItems":cartItems}
	return render(request,"base_app/checkout.html",context)