from rest_framework import serializers

from QandA.models import Vote, Answer, Question
from users.models import Profile

class VoteSerializer(serializers.Serializer):
    upvote = serializers.BooleanField(read_only=True)

    class Meta:
        model = Vote
        fields = ('upvote',)

class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    """  for main list display of Answers"""
    profile = serializers.HyperlinkedRelatedField(read_only=True, view_name='profile-detail')
    question = serializers.HyperlinkedRelatedField(read_only=True, view_name='question-detail')
    vote_set = VoteSerializer('vote_set', read_only=True)
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
        fields = ('profile', 'question', 'score', 'vote_set', 'upvotes', 'downvotes')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    """ for main list display of questions"""
    profile = serializers.HyperlinkedRelatedField(read_only=True, view_name='profile-detail')
    answer_set = AnswerSerializer('answer_set', read_only=True)
    #tag_set = TagSerializer('tag_set', read_only=True)

    class Meta:
        model = Question
        fields = ('profile', 'answer_set',)# 'tag_set')


class AnswerEditSerializer(serializers.Serializer):
    """ for editing and creation of Answers"""
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    vote_set = VoteSerializer('vote_set')

    class Meta:
        model = Answer
        fields = ('profile', 'question', 'vote_set')


    def create(self, validated_data):
        answer = Answer.objects.create(**validated_data)
        return answer

    def update(self, answer, validated_data):
        vote_set = validated_data.get('vote_set')

        if vote_set:
            vote_set = VoteSerializer(vote_set, many=True)
            if vote_set.is_valid():
                answer.vote_set.all().delete()
                answer.vote_set = vote_set.save()
                answer.save()

        return answer
