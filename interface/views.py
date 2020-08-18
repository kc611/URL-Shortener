
from django.shortcuts import render,redirect 
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from . forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from django.views import View
from . import models
# Create your views here.
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def check_url(url):
	validate = URLValidator()
	try:
		validate(url)
		
	except ValidationError as exception:
		return 0
	return 1

def base(request):

	if request.user.is_authenticated:
		return redirect('home')
	context = {}
	context['flag'] = 0

	if request.method == 'POST':
		print(request.POST.get('url_object'))
		url_obj = request.POST.get('url_object')
		if check_url(url_obj):
			new_obj = models.shorturl.objects.create(url = url_obj,user = "None")
			context['flag'] = 1
			context['object'] = new_obj
		else:
			context['invalid'] = url_obj
			context['flag'] = 2

		return render(request, 'interface/base.html',context)

	return render(request, 'interface/base.html',context)

def home(request):
	if request.user.is_authenticated:
		context={}
		
		
		if request.method == 'POST':
			print(request.POST.get('url_object'))
			url_obj = request.POST.get('url_object')
			if check_url(url_obj):
				new_obj = models.shorturl.objects.create(url = url_obj,user = request.user.username)
				
			context['user_urls'] = models.shorturl.objects.filter(user = request.user.username)
			return render(request, 'interface/home.html',context)
		context['user_urls'] = models.shorturl.objects.filter(user = request.user.username)
		return render(request, 'interface/home.html',context)
	else:
		return redirect('base')

@login_required(login_url='login')
def dashboard(request):
	return render(request, 'interface/user.html')

@login_required(login_url='login')
def urlinfo(request):
	return render(request, 'interface/urlinfo.html')

def logoutuser(request):
	logout(request)
	return redirect('base')

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(request,username=username,password=password)

			if user is not None:
				login(request,user)
				return redirect('home')


		context = {}
		return render(request, 'interface/login.html')

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()

		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				# username = request.POST.get('username')
				# password = request.POST.get('password')

				# user = authenticate(request,username=username,password=password)
				messages.success(request,'Account was created Sucessfully')
				return redirect('home')
			else:
				#Here display message that shit happend\ed
				pass
		

		context = {'form':form}
		return render(request, 'interface/register.html',context)

def redirect_views(request,*args,**kwargs):
    curr_id = kwargs['id']
    print(curr_id)
    try:
        curr_obj = models.shorturl.objects.get(shortened = curr_id)
    except:
        return HttpResponse("Sorry URL does not Exist")
    return HttpResponseRedirect(curr_obj.url)
