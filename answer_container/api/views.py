from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
# Create your views here.

from api.serializers import QuestionSerializer
from QandA.models import Question, Answer, Vote, Tag

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permissions_classes = (permissions.IsAuthenticatedOrReadOnly,)

    pagination_class = StandardResultsSetPagination


class AnswerViewSet(viewsets.ModelViewSet):
    pass
