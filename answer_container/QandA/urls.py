from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^questions/$', views.QuestionsView.as_view(), name='questions'),

]
