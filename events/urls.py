from django.conf.urls import  include, url
import views

urlpatterns = [
	url(r'^$', views.eventConsole),
	url(r'^create$', views.createEvent),
	url(r'^delete/(?P<eventID>\w{0,30})$',views.deleteEvent),

]