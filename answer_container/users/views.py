from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from users.forms import UserForm, ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from users.models import Profile
from QandA.models import Question, Answer

# Create your views here.

class AddUserView(View):

    def get(self, request):
        user_form = UserForm()
        profile_form = ProfileForm()
        return render(request, "register.html", {"form1": user_form, "form2": profile_form})

    def post(self, request):
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            password = user.password
            user.set_password(password)
            user.save()

            user = authenticate(username=user.username,
                                password=password)

            login(self.request, user)
            messages.add_message(
                request,
                messages.SUCCESS,
                "Account Successfully Created.")
            return redirect("qanda:questions")
        else:
            return render(request, "register.html", {"form1": user_form, "form2": profile_form})


class ShowProfileDetailView(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'profile.html'

    def get_object(self, queryset=None):
        return Profile.objects.get(pk=self.kwargs['prof_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.filter(profile=self.object).order_by('timestamp')
        answers = Answer.objects.filter(profile=self.object)
        score = self.object.get_score
        user = self.request.user
        if user == self.object.user:
            own = True
        else:
            own = False
        context['questions'] = questions
        context['answers'] = answers
        context['score'] = score
        context['own'] = own
        context['bio'] = self.object.bio
        return context
