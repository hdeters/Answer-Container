from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'^answers/', views.AnswerView.as_view(), name='answers')
