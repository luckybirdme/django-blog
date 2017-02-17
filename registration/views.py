from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from form import RegisterForm,LoginForm


# Create your views here.

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, password=password,email=email)
			user = authenticate(username=username, password=password)
			auth_login(request, user)
			return redirect(reverse('home'))

		else:
			return render(request, 'registration/register.html',{'form': form})
	else:
		form = RegisterForm()
		return render(request, 'registration/register.html',{'form': form})


def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			auth_login(request,user)
			return redirect(reverse('home'))
		else:
			form.add_error('username','username or password is not right')
			return render(request, 'registration/login.html',{'form': form})
	else:
		form = LoginForm()
		return render(request, 'registration/login.html',{'form': form})

def logout(request):
	auth_logout(request)
	return redirect(reverse('home'))
	
