from django.conf.urls import  include, url
import views

urlpatterns = [
	url(r'^create$', views.createTix),
	url(r'^delete/(?P<ticketGroupID>\w{0,30})$', views.deleteTixGroup),
]