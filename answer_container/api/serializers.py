from rest_framework import serializers
from django.contrib.auth.models import User

from QandA.models import Vote, Answer, Question
from users.models import Profile

class VoteSerializer(serializers.Serializer):
    upvote = serializers.BooleanField(read_only=True)

    class Meta:
        model = Vote
        fields = ('upvote',)


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    """  for main list display of Answers"""
    profile = serializers.HyperlinkedRelatedField(read_only=True, \
                                                  view_name='profile-detail')
    question = serializers.HyperlinkedRelatedField(read_only=True, \
                                                   view_name='question-detail')
    vote_set = VoteSerializer('vote_set', many=True, read_only=True)
    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    def get_upvotes(self, obj):
        return obj.vote_set.filter(upvote=True).count()

    def get_downvotes(self, obj):
        return obj.vote_set.filter(upvote=False).count()

    def get_score(self, obj):
        obj.set_score()
        return obj.score

    class Meta:
        model = Answer
        fields = ('url', 'profile', 'question', 'score', 'vote_set', \
                  'upvotes', 'downvotes')


class EditAnswerSerializer(serializers.Serializer):
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    text = serializers.CharField()
    vote_set = VoteSerializer('vote_set', many=True)

    class Meta:
        model = Answer
        fields = ('profile', 'text', 'vote_set')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.HyperlinkedRelatedField(read_only=True, \
                                                  view_name='profile-detail')
    title = serializers.CharField()
    text = serializers.CharField()
    answer_set = EditAnswerSerializer('answer_set', many=True, read_only=True)
    #tag_set = TagSerializer('tag_set', read_only=True)

    class Meta:
        model = Question
        fields = ('url', 'profile', 'title', 'text', 'answer_set',)# 'tag_set')

    def create(self, validated_data):
        profile = Profile.objects.get(user=self.request.user)
        question = Question.objects.create(profile=profile, **validated_data)
        return question

    def update(self, question, validated_data):
        options = ['title', 'text']
        for item in options:
            if validated_data.get(item):
                question[item] = validated_data['item']

        if validated_data.get('answer_set'):
            answer_set = validated_data['answer_set']
            question.answer_set.all().delete()
            for item in answer_set:
                question.answer_set.create(**item)

        question.save()
        return question


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(source='user.username')
    question_set = serializers.HyperlinkedRelatedField(many=True, \
                                                    read_only=True, \
                                                    view_name='question-detail')
    answer_set = serializers.HyperlinkedRelatedField(many=True, \
                                                     read_only=True, \
                                                     view_name='answer-detail')

    class Meta:
        model = Profile
        fields = ('url', 'username', 'question_set', 'answer_set',)
