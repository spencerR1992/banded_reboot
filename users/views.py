from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseBadRequest

# Create your views here.


def authorization(request):
	try:
		em = request.POST.get('email', '')
		print 'em: ', em
		pw = request.POST.get('password', '')
		print 'pw: ', pw
		user = authenticate(email = em, password = pw)
		if user is not None:
			print 'user successfully logged in'
			return render(request, 'home.html')
		else:
			print 'login failed'
			return render(request, 'home.html')
	except Exception, e:
		return HttpResponseBadRequest(str(e), status = 400)



