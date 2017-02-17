from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^home/',
        views.home,
        name='home'),
    url(r'^draft/',
        views.draft,
        name='draft'),
   	url(r'^user/(?P<username>\w+)/$',
        views.user,
        name='user'),
   	url(r'^tag/(?P<tag>\w+)/$',
        views.tag,
        name='tag'),
    url(r'^alluser/', views.alluser, name='alluser'),
    url(r'^alltag/', views.alltag, name='alltag'),
    url(r'^write/', views.write, name='write'),
    url(r'^search/', views.search, name='search'),
    url(r'^upload/', views.upload, name='upload'),
    url(r'^comment/', views.comment, name='comment'),
    url(r'^show/(?P<id>\d+)/$', views.show, name='show'),
]
