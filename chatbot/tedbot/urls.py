from django.conf.urls import url

from tedbot import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^chatanalytics/$', views.chatanalytics, name='chatanalytics'),
	url(r'^elimuhome/$', views.elimuhome, name='elimuhome'),
	url(r'^housing/$', views.housing, name='housing'),
	url(r'^scholarships/$', views.scholarships, name='scholarships'),
] 