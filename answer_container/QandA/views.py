from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, UpdateView, CreateView, ListView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime

from QandA.forms import AnswerCreateForm
from QandA.models import Question, Answer


@login_required
def upvote(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    answer.vote_set.create(profile=request.user.profile, upvote=True)

    return redirect('qanda:question', pk=answer.question.pk)


@login_required
def downvote(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    answer.vote_set.create(profile=request.user.profile, upvote=False)

    return redirect('qanda:question', pk=answer.question.pk)


class Questions(ListView):
    model = Question
    template_name = 'QandA/question_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Question.objects.all().order_by('-timestamp')


class QuestionDetail(DetailView):
    model = Question

    def get_context_data(self, object):
        context = super().get_context_data()
        answers = object.answer_set.all()
        for item in answers:
            item.set_score()
            item.save()

            if item.vote_set.filter(profile=self.request.user.profile).exists():
                item.voted = True

        context['answers'] = answers.order_by('-score')

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
            question.answer_set.create(text=form['text'].value(), \
                                       profile=request.user.profile)

            return redirect('qanda:question', pk=question.pk)

        context['form_errors'] = form.errors
        return render(request, 'QandA/answer-create.html', context)
