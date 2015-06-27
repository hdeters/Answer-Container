from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^questions/$', views.Questions.as_view(), name='questions'),
    url(r'^questions/(?P<pk>[0-9]+)$', views.QuestionDetail.as_view(), \
        name='question'),
    url(r'^question/(?P<pk>[0-9]+)/answer/', views.CreateAnswer.as_view(), name='answer'),
    url(r'^question/$', views.CreateQuestion.as_view(), name='question-create'),
    url(r'^upvote/(?P<pk>[0-9]+)', views.upvote, name='upvote'),
        url(r'^downvote/(?P<pk>[0-9]+)', views.downvote, name='downvote'),
]
