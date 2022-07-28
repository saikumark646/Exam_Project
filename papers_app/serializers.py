from rest_framework import serializers
from .models import *
from rest_framework import pagination

class SmallSetPagination(pagination.PageNumberPagination):
    page_size = 1

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
        
    def to_representation(self,instance):
        return {
            'id':instance.id,
            'user_id':instance.user.id,
            'username':instance.user.username,
            'firstname':instance.user.first_name,
            'lastname':instance.user.last_name,
            'email':instance.user.email,
            'profile_choice': instance.profile_choice,
            'subject':instance.subject.subject_name if instance.subject else None,
            'mobile_number':instance.mobile_number
        }
class SubjectSerializer(serializers.ModelSerializer):
    class Meta :
        model = Subject
        fields = '__all__'
        
class QuestionSerializer(serializers.ModelSerializer):
    class Meta :
        model = Question
        fields = '__all__'
class AnswerSerializer(serializers.ModelSerializer):
    class Meta :
        model = Answer
        fields = '__all__'
        
class TestPaperSerializer(serializers.ModelSerializer):
    class Meta :
        model = TestPaper
        fields = '__all__'
        
class CheckingTestPaperSerializer(serializers.ModelSerializer):
    class Meta :
        model = TestPaper
        fields = '__all__'     
        