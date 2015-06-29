from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView, CreateView, ListView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.urlresolvers import reverse, reverse_lazy
import pytz

import datetime

from QandA.forms import AnswerCreateForm, CommentCreateForm
from QandA.models import Question, Vote, Answer, Comment


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
        return Question.objects.all().annotate(ans_count=Count('answer')).order_by('-timestamp')


class QuestionDetail(DetailView):
    model = Question

    def get_context_data(self, object):
        context = super().get_context_data()
        answers = object.answer_set.all().prefetch_related()
        for answer in answers:
            answer.set_score()
            answer.save()

        answers_sorted = list(answers.order_by('-score'))

        own = False

        if self.request.user.is_authenticated():
            context['votes'] = [item['answer'] for item in \
                                self.request.user.profile.vote_set.values('answer')]

            if object.profile == self.request.user.profile:
                own = True

        if pytz.utc.localize(datetime.datetime.utcnow()) > (object.timestamp + datetime.timedelta(minutes=10)):
            update_delete_question = False
        elif answers.count() >= 1:
            update_delete_question = False
        else:
            update_delete_question = True

        comment_pks = []
        for comment in Comment.objects.all():
            comment_pks.append(int(comment.answer.pk))

        update_delete_answer = []

        for answer in answers:
            if pytz.utc.localize(datetime.datetime.utcnow()) > (answer.timestamp + datetime.timedelta(minutes=10)):
                update_delete_answer.append(False)
            elif answer.vote_set.count() >= 1:
                update_delete_answer.append(False)
            elif answer.pk in comment_pks:
                update_delete_answer.append(False)
            else:
                update_delete_answer.append(True)


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


class QuestionUpdate(UpdateView):
    model = Question
    fields = ['title', 'text']
    template_name = 'QandA/question_update_form.html'

    def get_success_url(self):
        return reverse('qanda:question', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None, **kwargs):
        question = Question.objects.get(id=self.kwargs['pk'])
        return question

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        messages.add_message(self.request, messages.SUCCESS,
                             "Your question was successfully updated!")
        return super(QuestionUpdate, self).form_valid(form)


class QuestionDelete(DeleteView):
    model = Question

    def get_success_url(self):
        return reverse_lazy('qanda:questions')

    def get_object(self, queryset=None):
        return Question.objects.filter(pk=self.kwargs['pk'])

    def get_template_names(self):
        return 'QandA/question_confirm_delete.html'


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
            question.answer_set.create(text=form['text'].value(), timestamp=datetime.datetime.utcnow(),
                                       profile=request.user.profile)

            return redirect('qanda:question', pk=question.pk)

        context['form_errors'] = form.errors
        return render(request, 'QandA/answer-create.html', context)


class AnswerUpdate(UpdateView):
    model = Answer
    fields = ['text']
    template_name = 'QandA/answer_update_form.html'

    def get_object(self, queryset=None, **kwargs):
        answer = Answer.objects.get(id=self.kwargs['pk'])
        return answer

    def get_success_url(self):
        return reverse('qanda:question', kwargs={'pk': self.object.question.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        messages.add_message(self.request, messages.SUCCESS,
                             "Your answer was successfully updated!")
        return super(AnswerUpdate, self).form_valid(form)


class AnswerDelete(DeleteView):
    model = Answer

    def get_success_url(self):
        return reverse_lazy('qanda:questions')

    def get_object(self, queryset=None):
        return Answer.objects.filter(pk=self.kwargs['pk'])

    def get_template_names(self):
        return 'QandA/answer_confirm_delete.html'


class AcceptAnswer(TemplateView):
    def get(self, request, ans_pk, q_pk):
        question = get_object_or_404(Question, pk=q_pk)
        question.accepted_answer = ans_pk
        question.save()
        context = self.get_context_data()
        context['q_pk'] = q_pk
        return render(request, 'QandA/accept_answer.html', context)


class CreateComment(CreateView):
    model = Comment
    fields = ['text', ]

    def get(self, request, pk):
        return super().get(request)

    @method_decorator(login_required)
    def post(self, request, pk):
        text = request.POST['text']
        answer = Answer.objects.get(pk=self.kwargs['pk'])
        question_pk = answer.question.pk

        Comment.objects.create(text=text, \
                               profile=request.user.profile, \
                               answer=answer)

        return redirect('qanda:question', pk=question_pk)
