from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBadRequest
from models import EventUser
from django.contrib.auth.models import User

# Create your views here.

#TODO:remove print statements, and properly handle the redirect. 
def authorization(request):
	try:
		em = request.POST['email']
		pw = request.POST['password']
		err_message = []
		if (em == ''):
			err_message.append('Please provide an email')
		if (pw == ''):
			err_message.append('Please enter your password!')
		if (len(err_message)>0):
			return render(request, 'home.html', {'login_errors':err_message})
		else:
			user = authenticate(email = em, password = pw)
			if user is not None:
				login(request, user)
				return redirect('/')
			else:
				print 'login failed'
				return render(request, 'home.html', {'login_errors':['The username or password you provided was incorrect']})
	except Exception, e:
		return HttpResponseBadRequest(str(e), status = 400)


def logOut(request):
	logout(request)
	return redirect('/')


def createUser(request):
	try:
		em = str(request.POST['email'])
		pw = str(request.POST['password'])
		error = False
		err_message = []
		try:
			if ((len(em)<5) or ("@" not in em)):
				error = True
				err_message.append('Please provide a valid username')
			else:
				User.objects.get(email = em)
				error = True
				err_message.append('That username is already taken!')	
		except: 
			pass
		try: 
			if (len(pw)<7):
				error = True
				err_message.append('Password length is too short')
		except:
			error = True
			err_message.append('Please provide a password')
		if error:
			return render(request, 'home.html', {'registration_errors': err_message})
		user = User.objects.create_user(em, em, pw)
		user.save()
		user = EventUser(user = user)
		o_n = request.POST['organization_name']
		if o_n:
			if 'optional' not in o_n:
				user.organization_name = o_n
		user.save()
		user = authenticate(email = em, password = pw)
		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			print 'login failed'
			return render(request, 'home.html')
	except Exception, e:
		return HttpResponseBadRequest(str(e), status=400)




