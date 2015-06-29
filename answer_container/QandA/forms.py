from django import forms

from QandA.models import Answer, Comment

class AnswerCreateForm(forms.Form):
    text = forms.CharField(required=True)

    class Meta:
        model = Answer
        fields = ('text',)

class CommentCreateForm(forms.Form):
    text = forms.CharField(required=True)

    class Meta:
        model = Comment
        fields = ('text',)
