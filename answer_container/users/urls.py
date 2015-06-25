from django.contrib.auth import views
from django.conf.urls import include, url
from users import views as users_views


urlpatterns = [
    url(r'^login/$', views.login, {'template_name': 'login.html'}, name="login"),
    url(r'^logout/$', views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^register/$', users_views.AddUserView.as_view(), name="user_register"),
]