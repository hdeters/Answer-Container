from django.conf.urls import include, url
from rest_framework import routers

from . import views


router = routers.DefaultRouter()

router.register(r'answers', views.AnswerViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'profiles', views.ProfileViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
