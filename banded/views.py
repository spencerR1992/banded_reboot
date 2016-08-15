from django.shortcuts import render
from django.template.context import RequestContext



'''
Holders for testing endpoints. This will eventually only be home to the '/' 
view.

'''
def home(request):
	return render(request, 'home.html')

def loginTest(request):
	return render(request, 'login.html')

def styleSheet(request):
	return render(request, 'style_sheet.html')