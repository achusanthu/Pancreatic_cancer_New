from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

from .models import *
from django.contrib.auth import authenticate , login ,logout
#from django.contrib.auth.models import User
from django.conf import settings
from django.views import generic
# from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
import os
# Create your views here.
def index(request):
	return render(request,'index.html')

def about(request):
	return render(request,'about.html')

def contact(request):
	return render(request,'contact.html')
def userpredict(request):
	return render(request,'user_predict.html')

def log_in(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(username=email,password=password)
		if user:
			print (user)

			login(request,user)
			return render(request,'user_predict.html', {"msg3":'Login Successfully'})
		else:
			# error="sorry"
			return render(request,'signin.html',{"msg2":'UNABLE TO LOGIN '})
	else:
		return render(request,'signin.html',{})
	# else:
	#   return render(request,'login.html',{})  
	return render(request,'signin.html',{})		


def register(request):
	if request.method=='POST':
		name = request.POST.get('name')
		mobile = request.POST.get('phone')
		psw1 = request.POST.get('psw')
		psw2 = request.POST.get('psw1')
		email = request.POST.get('email')
		username=request.POST.get('username')
		if psw1==psw2:
			user1=UserProfile.objects.filter(email=email,password=psw1).exists()
		else:
			messages.warning(request,'not matching password')	
		if not user1:   
			user2=User.objects.create_user(
				username=email,
				password=psw1,
				)
			
			user_pro=UserProfile.objects.create(
				user=user2,
				email=email,
				password=psw1,
				mobile=mobile,
				name=name,
				username=username,
			)
			user_pro.save()
			return render(request,'signin.html',{"msg1":'you are logined'})
		else:
			messages.warning(request,'username already exist sorry try again')
			return render(request,'index.html',{'error':error})


			
	return render(request,'register.html',{})

def getPredictions(number,age,	sex, stage,	plasma_CA19_9,	creatinine,	LYVE1,	REG1B,	TFF1,REG1A):
    import pickle
    model = pickle.load(open("C:/Users/test/Desktop/Pancreatic_cancer_New/Pancreatic_cancer/cancer/pan.sav", "rb"))
    scaled = pickle.load(open("C:/Users/test/Desktop/Pancreatic_cancer_New/Pancreatic_cancer/cancer/scaler.sav", "rb"))
    prediction = model.predict(scaled.transform([[number,age,sex, stage,plasma_CA19_9,	creatinine,	LYVE1,REG1B,TFF1, REG1A]]))
    
    if prediction == 1:
        return "Your pancrease is safe"
    elif prediction == 2:
        return "Sorry you have Minor Pancreatic disease"
    elif prediction == 3:
        return "Sorry you have Major Pancreatic disease"
    else:
        return "error"
        

# our result page view
def result(request):
	number = int(request.GET['number'])
	age = int(request.GET['age'])
	sex = int(request.GET['sex'])
	stage = int(request.GET['stage'])
	plasma_CA19_9 = float(request.GET['plasma'])
	creatinine = float(request.GET['creatinine'])
	LYVE1 = float(request.GET['LYVE1'])
	REG1B = float(request.GET['REG1B'])
	TFF1 = float(request.GET['TFF1'])
	REG1A = float(request.GET['REG1A'])

	result = getPredictions(number,age, sex, stage, plasma_CA19_9,	creatinine,	LYVE1,	REG1B,	TFF1, REG1A)

	return render(request, 'result.html', {'result':result})