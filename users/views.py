from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBadRequest

# Create your views here.

#TODO:remove print statements, and properly handle the redirect. 
def authorization(request):
	try:
		em = request.POST['email']
		pw = request.POST['password']
		user = authenticate(email = em, password = pw)
		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			print 'login failed'
			return render(request, 'home.html')
	except Exception, e:
		return HttpResponseBadRequest(str(e), status = 400)


def logOut(request):
	logout(request)
	return redirect('/')



