from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^questions/$', views.Questions.as_view(), name='questions'),
    url(r'^questions/(?P<pk>[0-9]+)$', views.QuestionDetail.as_view(), \
        name='question'),
    url(r'^question/(?P<pk>[0-9]+)/answer/', views.CreateAnswer.as_view(), name='answer'),
    url(r'^accept/(?P<ans_pk>[0-9]+)/(?P<q_pk>[0-9]+)/', views.AcceptAnswer.as_view(), name='accept_answer'),
    url(r'^question/$', views.CreateQuestion.as_view(), name='question-create'),
    url(r'^upvote/(?P<pk>[0-9]+)', views.upvote, name='upvote'),
        url(r'^downvote/(?P<pk>[0-9]+)', views.downvote, name='downvote'),
    url(r'^update_question/(?P<pk>\d*)$', views.QuestionUpdate.as_view(), name="update_question"),
    url(r'^update_answer/(?P<pk>\d*)$', views.AnswerUpdate.as_view(), name="update_answer"),
    url(r'^delete_question/(?P<pk>\d+)$', views.QuestionDelete.as_view(), name='delete_question'),
    url(r'^delete_answer/(?P<pk>\d+)$', views.AnswerDelete.as_view(), name='delete_answer'),
    url(r'^add_comment/(?P<pk>\d+)/$', views.CreateComment.as_view(), name="create_comment"),
]
