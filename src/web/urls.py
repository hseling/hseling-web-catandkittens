from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.web_index, name='index'),
    url(r'^main$', views.web_main, name='main'),
    url(r'^upload$', views.web_upload_file, name='upload'),
    url(r'^status$', views.web_status, name='status'),
    url(r'^check$', views.web_check, name='check'),
    url(r'^collocations$', views.web_collocations, name='collocations'),
    url(r'^intext$', views.web_intext, name='intext'),
    url(r'^search$', views.web_search, name='search'),
    url(r'^search_morph$', views.web_search_morph, name='search_morph'),
    url(r'^search_collocations$', views.web_search_collocations, name='search_collocations')
]
