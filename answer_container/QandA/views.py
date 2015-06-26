from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, UpdateView, CreateView, ListView
from django.views.generic.detail import DetailView
from QandA.models import Question, Vote, Answer
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import datetime

from QandA.forms import AnswerCreateForm


class Questions(ListView):
    model = Question
    template_name = 'QandA/question_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Question.objects.all().annotate(ans_count=Count('answer')).order_by('-timestamp')

    # def get_context_data(self):
    #     context = super().get_context_data()
    #     answer_count = Question.objects.annotate(ans_count=Count('answer'))
    #     context['answer_count'] = answer_count
    #     return context


class QuestionDetail(DetailView):
    model = Question

    def get_context_data(self, object):
        context = super().get_context_data()
        context['answers'] = object.answer_set.all()
        if object.profile == self.request.user.profile:
            own = True
        else:
            own = False
        context['own'] = own
        return context


class CreateQuestion(CreateView):
    model = Question
    fields = ['title', 'text']

    @method_decorator(login_required)
    def get(self, request):
        return super().get(request)

    @method_decorator(login_required)
    def post(self, request):
        title = request.POST['title']
        text = request.POST['text']

        Question.objects.create(title=title, text=text, \
                                profile=request.user.profile, \
                                timestamp=datetime.datetime.utcnow())

        return redirect('users:profile', prof_id=request.user.profile.pk)

class CreateAnswer(TemplateView):
    @method_decorator(login_required)
    def get(self, request, pk):
        form = AnswerCreateForm()
        question = get_object_or_404(Question, pk=pk)
        context = self.get_context_data()
        context['question'] = question
        context['profile'] = request.user.profile
        context['form'] = form
        return render(request, 'QandA/answer-create.html', context)

    @method_decorator(login_required)
    def post(self, request, pk):
        form = AnswerCreateForm(request.POST)
        if form.is_valid():
            question = get_object_or_404(Question, pk=pk)
            question.answer_set.create(text=form['text'], \
                                       profile=request.user.profile)

            return redirect('qanda:question', pk=question.pk)

        context['form_errors'] = form.errors
        return render(request, 'QandA/answer-create.html', context)


class AcceptAnswer(TemplateView):
    def get(self, request, ans_pk, q_pk):
        question = get_object_or_404(Question, pk=q_pk)
        question.accepted_answer = ans_pk
        question.save()
        context = self.get_context_data()
        context['q_pk'] = q_pk
        return render(request, 'QandA/accept_answer.html', context)

