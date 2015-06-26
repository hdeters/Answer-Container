from .models import Question, Answer, Vote, Profile
from django.contrib import admin

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'profile']

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'profile', 'question', 'score']

class VoteAdmin(admin.ModelAdmin):
    list_display = ['profile', 'answer', 'upvote']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'get_score']

# Register your models here.

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Profile, ProfileAdmin)
