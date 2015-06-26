from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, UpdateView, CreateView, ListView
from django.views.generic.detail import DetailView
from QandA.models import Question
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from QandA.forms import AnswerCreateForm


class Questions(ListView):
    model = Question
    template_name = 'QandA/question_list.html'
    paginated_by = 10

    def get_queryset(self):
        return Question.objects.all().order_by('-timestamp')


class QuestionDetail(DetailView):
    model = Question

    def get_context_data(self, object):
        context = super().get_context_data()
        context['answers'] = object.answer_set.all()
        return context


class CreateQuestion(CreateView):
    model = Question
    fields = ['title', 'text']

    @method_decorator(login_required)
    def get(self):
        return super().get()

    @method_decorator(login_required)
    def post(self):
        return super.get()


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
        form = AnswerCreateForm(request.POST['form'])
        if form.is_valid():
            question = get_object_or_404(Question, pk=pk)
            form.save(commit=False)
            question.answer_set.create(text=form.text, \
                                       profile=request.user.profile)

            return redirect('QandA:question', pk=question.pk)

        context['form_errors'] = form.errors
        return render(request, 'QandA/answer-create.html', context)
