from django.conf.urls import url , include
from . import views

urlpatterns = [
    url(r'^login/$', views.Login),
    url(r'^register/$', views.Register),
    url(r'^logout/$', views.Logout),
    url(r'^activate/(?P<key>.+)/$', views.Activate),
    url(r'^edit_profile/$', views.Edit_profile)
]
