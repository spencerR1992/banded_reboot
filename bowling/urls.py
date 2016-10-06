from django.conf.urls import  include, url
import views

urlpatterns = [
	# url(r'^$', views.eventConsole),
	# url(r'^delete/(?P<eventID>\w{0,30})$',views.deleteEvent),
	url(r'^game$', views.gameBase),
	url(r'^game/(?P<gameID>\w{0,30})$', views.gameMain),
	# url(r'^(?P<hashCode>\w{0,40})$', views.ticketClaim),
]