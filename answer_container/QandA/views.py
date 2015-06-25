from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, UpdateView, CreateView, ListView
from django.views.generic.detail import DetailView
from QandA.models import Question


class QuestionsView(ListView):
    model = Question
    template_name = 'QandA/question-list.html'
    paginated_by = 10

    def get_queryset(self):
        Question.objects.all().order_by('-timestamp')


class QuestionDetail(DetailView):
    model = Question
    

class CreateQuestionView(CreateView):
    model = Question
    fields = ['title', 'text']
