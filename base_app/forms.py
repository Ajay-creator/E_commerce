from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ShippingAddress


class CreateUserForm(UserCreationForm):

	class Meta:
		model = User
		fields = ["username","email","password1","password2"]


class AddressForm(ModelForm):

	class Meta:
		model = ShippingAddress
		fields = '__all__'
		exclude = ['customer','product']