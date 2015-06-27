from django.conf.urls import include, url
from rest_framework import routers

from . import views


router = routers.DefaultRouter()

#router.register(r'^answer', views.AnswerViewSet)
router.register(r'question', views.QuestionViewSet)
router.register(r'profile', views.ProfileViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
