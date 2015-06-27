from django import forms

from QandA.models import Answer

class AnswerCreateForm(forms.Form):
    text = forms.CharField(required=True)

    class Meta:
        model = Answer
        fields = ('text',)
