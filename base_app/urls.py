from django.urls import path
from . import views

urlpatterns = [
path('',views.home,name="home"),
path('signup/',views.SignupPage,name="signup"),
path('login/',views.LoginPage,name="login"),
path('logout/',views.LogoutUser,name="logout"),
path('mensFashion/',views.MensFashionPage,name="MenFashion"),
path('womensFashion/',views.WomensFashionPage,name="WomenFashion"),
path('order/',views.OrderPage,name="order"),
path('my_cart/',views.Cart,name="my_cart"),
path('checkout/',views.Checkout,name="checkout"),
path('update_cart/',views.UpdateItem,name="update_cart"),
]