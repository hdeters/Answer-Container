from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^questions/$', views.QuestionsView.as_view(), name='questions'),
    url(r'^questions/(?P<pk>[0-9]+)$', views.QuestionDetail.as_view(), \
        name='question'),
]
