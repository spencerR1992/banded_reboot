from django.conf.urls import  include, url
import views

urlpatterns = [
	url(r'^auth$', views.authorization),
]