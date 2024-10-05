# DJANGO LIBRARIES
from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.db.models import Q
import json
from cart.cart import Cart
#REST Library
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from .permissions import IsAdminOrReadOnly
from payment.models import Order, OrderItem
from .serializers import ProfileSerializer, ProductSerializer, CategorySerializer, OrderSerializer, OrderItemSerializer



#API STUFF


class APIRootView(APIView):
    """
    Home page for the API that lists all available endpoints, including detail views.
    """
    def get(self, request, *args, **kwargs):
        return Response({
            'products': {
                'list': reverse('api_product', request=request),
                'details': 'Example: ' + reverse('api_product_details', kwargs={'pk': 4}, request=request),
            },
            'categories': {
                'list': reverse('api_category', request=request),
                'details': 'Example: ' + reverse('api_category_details', kwargs={'pk': 4}, request=request),
            },
            'profiles': {
                'list': reverse('api_profile', request=request),
                'details': 'Example: ' + reverse('api_profile_details', kwargs={'pk': 4}, request=request),
            },
            'orders': {
                'list': reverse('api_order', request=request),
                'details': 'Example: ' + reverse('api_order_details', kwargs={'pk': 4}, request=request),
            },
            'order-items': {
                'list': reverse('api_order_item', request=request),
                'details': 'Example: ' + reverse('api_order_item_details', kwargs={'pk': 4}, request=request),
            },
        })


class ProductList(generics.ListCreateAPIView):
	serializer_class = ProductSerializer

	def get_queryset(self):
		queryset = Product.objects.all()
		category = self.request.query_params.get('category')
		if category:
			queryset = Product.objects.filter(category=category)
		return queryset
	permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
	

class ProductDetails(generics.RetrieveUpdateDestroyAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
	
	
class CategoryList(generics.ListCreateAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class CategoryDetails(generics.RetrieveUpdateDestroyAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class ProfileList(generics.ListCreateAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer
	permission_classes = [IsAuthenticated, IsAdminOrReadOnly]	


class ProfileDetails(generics.RetrieveUpdateDestroyAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer
	permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class OrderList(generics.ListCreateAPIView):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	permission_classes = [IsAuthenticated, IsAdminOrReadOnly]	


class OrderDetails(generics.RetrieveUpdateDestroyAPIView):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	permission_classes = [IsAuthenticated, IsAdminOrReadOnly]	


class OrderItemList(generics.ListCreateAPIView):
	serializer_class = OrderItemSerializer

	def get_queryset(self):
		queryset = OrderItem.objects.all()
		order = self.request.query_params.get('order')
		if order:
			queryset = OrderItem.objects.filter(order=order)
		return queryset
	permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class OrderItemDetails(generics.RetrieveUpdateDestroyAPIView):
	queryset = OrderItem.objects.all()
	serializer_class = OrderItemSerializer
	permission_classes = [IsAuthenticated, IsAdminOrReadOnly]	



#DJANGO STUFF



def search(request):
	if request.method == 'POST':
		searched = request.POST['searched']
		searched = Product.objects.filter(Q(name__icontains = searched) | Q(category__name__icontains = searched))

		if not searched:
			messages.success(request, "That product is not exist. Please try find another product.")
			return render(request, 'search.html', {})
		else:
			return render(request, 'search.html', {'searched':searched})
	else:
		return render(request, 'search.html', {})


def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "user has been updated")
			return redirect('home')
		return render(request, 'update_user.html', {'user_form': user_form})
	else:
		messages.success(request, "You must be logged in to access this page")
		return redirect('home')
	

def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		if request.method == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, 'Your password has been updated')
				return redirect('update_user')
			else:
				for err in list(form.errors.values()):
					messages.error(request, err)
					return redirect('update_password')

		else:
			form = ChangePasswordForm(current_user)
			return render(request, 'update_password.html', {'form':form})
	else:
		messages.success(request, "You must be logged in to access this page")
		return redirect('home')


def update_info(request):
	if request.user.is_authenticated:
		current_user = Profile.objects.get(user__id=request.user.id)
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

		#get orginial form
		form = UserInfoForm(request.POST or None, instance=current_user)
		#get user shipping form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

		if form.is_valid() or shipping_form.is_valid():
			form.save()
			shipping_form.save()

			messages.success(request, "Your info has been updated")
			return redirect('home')
		return render(request, 'update_info.html', {'form': form, 'shipping_form':shipping_form})
	else:
		messages.success(request, "You must be logged in to access this page")
		return redirect('home')
	

def category(request, cat):
	cat = cat.replace('-',' ').title()
	try:
		category = Category.objects.get(name=cat)
		products = Product.objects.filter(category=category)
		return render(request, 'category.html', {'products':products, 'category':category})
	except:
		messages.success(request, ("That category is not exist"))
		return redirect('home')
	

def category_summary(request):
	categories = Category.objects.all()
	return render(request, 'category_summary.html', {'categories':categories})


def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)

			#load shopping cart data
			current_user = Profile.objects.get(user__id = request.user.id)
			saved_cart = current_user.old_cart
			if saved_cart:
				converted_cart = json.loads(saved_cart)
				cart = Cart(request)
				for key, value in converted_cart.items():
					cart.db_add(product=key, quantity=value)

			messages.success(request, ("You Have Been Logged In!"))
			return redirect('home')
		else:
			messages.success(request, ("There was an error, please check your username and your password"))
			return redirect('login')

	else:
		return render(request, 'login.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out!"))
	return redirect('home')


def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Account created, please fill the billing info..."))
			return redirect('update_info')
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('register')
	else:
		return render(request, 'register.html', {'form':form})



