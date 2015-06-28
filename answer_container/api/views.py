from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
# Create your views here.

from api.serializers import QuestionSerializer, ProfileSerializer, \
                            AnswerSerializer
from QandA.models import Question, Answer, Vote, Tag
from users.models import Profile


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permissions_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = StandardResultsSetPagination
    allowed_methods = ['GET', 'POST', 'PUT', 'DELETE']


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permissions_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = StandardResultsSetPagination


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permissions_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = StandardResultsSetPagination
