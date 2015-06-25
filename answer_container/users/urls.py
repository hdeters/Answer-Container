from django.contrib.auth import views
from django.conf.urls import include, url


urlpatterns = [
    url(r'^login/$', views.login, {'template_name': 'login.html'}, name="login"),
    url(r'^logout/$', views.logout, {'next_page': 'login'}, name='logout'),
]