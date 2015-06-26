from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^questions/$', views.Questions.as_view(), name='questions'),
    url(r'^questions/(?P<pk>[0-9]+)$', views.QuestionDetail.as_view(), \
        name='question'),
    url(r'^question/(?P<pk>[0-9]+)/answer/', views.CreateAnswer.as_view(), name='answer'),
    url(r'^accept/(?P<ans_pk>[0-9]+)/(?P<q_pk>[0-9]+)/', views.AcceptAnswer.as_view(), name='accept_answer'),
    url(r'^question/$', views.CreateQuestion.as_view(), name='question-create'),
]
