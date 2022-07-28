from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import Question, Answer, Subject, TestPaper,Profile
from django.db.models import Q
from .serializers import *
from .permissions import IsUserAuthOrSameUser
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView,CreateAPIView
from rest_framework.viewsets import ModelViewSet
from django.db.models import Sum

User = get_user_model()


class ProfileCreation(APIView): 
    def get(self,request):
        profiles = self.get_queryset()
        serializer = ProfileSerializer(profiles, many = True)
        return Response(serializer.data) 
    
    def get_queryset(self):
        queryset = Profile.objects.all()
        username = self.request.query_params.get('username',None)
        if username is not None:
            queryset = queryset.filter(user__username = username)
        return queryset

    def post(self,request):
        params = request.data

        if 'username' not in params :
            return Response({"message":'username is manadatory field '},status = status.HTTP_400_BAD_REQUEST)
        username = params['username']
        if 'first_name' not in params :
            return Response({"message":'firstname is manadatory field '},status = status.HTTP_400_BAD_REQUEST)
        first_name = params['first_name']
        if 'last_name' not in params :
            return Response({"message":'lastname is manadatory field '},status = status.HTTP_400_BAD_REQUEST)
        last_name = params['last_name']
        if 'mobile_number' not in params :
            return Response({"message":'mobile_number is manadatory field '},status = status.HTTP_400_BAD_REQUEST)
        mobile_number = params['mobile_number']
        if 'profile_choice' not in params :
            return Response({"message":'profile_choice is manadatory field '},status = status.HTTP_400_BAD_REQUEST)
        profile_choice = params['profile_choice']
        if 'subject' not in params :
            return Response({"message":'subject is manadatory field '},status = status.HTTP_400_BAD_REQUEST)
        subject = params['subject']
        if 'email' not in params :
            return Response({"message":'email is manadatory field '},status = status.HTTP_400_BAD_REQUEST)
        email = params['email']
        lookup = Q(mobile_number=mobile_number) or Q(user__email  = email)
        if Profile.objects.filter(lookup).exists():
            return Response({"message":'email/mobile number is already exist '},status = status.HTTP_400_BAD_REQUEST)
        transaction.set_autocommit(autocommit=False)
        user_obj = User.objects.create(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email)
        user_obj.set_password(params['password'])
        user_obj.save()
        profile_obj = Profile.objects.create(
            user = user_obj,
            profile_choice = profile_choice,
            subject_id = subject,
            mobile_number = mobile_number
        )
        profile_obj.save()
        transaction.commit()
        serializer = ProfileSerializer(profile_obj, many = False).data
        print(serializer)
        return Response(serializer,status=status.HTTP_201_CREATED),
    
    
class ProfileDetail(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsUserAuthOrSameUser]
    
class SubjectList(ListCreateAPIView):
    queryset = Subject.objects.filter(is_active = True,is_delete = False)
    serializer_class = SubjectSerializer
    pagination_class = SmallSetPagination
    
# class QueationCreateView(ListCreateAPIView):
#     queryset = Question.objects.filter(is_active = True,is_delete = False)
#     serializer_class = QuestionSerializer
    
# class QueationDetailCreateView(RetrieveUpdateDestroyAPIView):
#     queryset = Question.objects.filter(is_active = True,is_delete = False)
#     serializer_class = QuestionSerializer
    
class QueationCreateView(APIView):
    # def get(self,request):
    #     questions = Question.objects.filter(is_active = True,is_delete = False)
    #     serializer = QuestionSerializer(questions, many = True)
    #     return Response(serializer.data)
    questions = Question.objects.filter(is_active = True,is_delete = False)
    model = Question
    def get(self,request):
        params = request.query_params
        if not params:
            return Response("required parameter ")
        fields = {}
        if 'subject' in params:
            fields['subject_id'] = params['subject']  # ?subject=1
        if 'user' in params:
            fields['creater_id'] = params['user'] # ?user=5
        if 'search' in params:
            fields['question__icontains' ] = params['search'] # ?search=where
        if 'question_id' in params:
            question_obj = self.questions.filter(id = params['question_id'])
        else:
            question_obj = self.questions.filter(**fields)
        
        data = QuestionSerializer(question_obj,many =True).data
        return Response(data, status = status.HTTP_200_OK)
    
    def post(self,request,*args, **kwargs):
        data = request.data
        print(data)
        if 'question' not in data:
            return Response({'message':'question is required field'},status = status.HTTP_400_BAD_REQUEST)
        question = data['question']
        if 'answer' not in data:
            return Response({'message':'answer is required field'},status = status.HTTP_400_BAD_REQUEST)
        answer = data['answer']
        lookup = Q(question = question)
        if Question.objects.filter(lookup).exists():
            return Response({'message':'question is already exist'},status = status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(profile__profile_choice = 'Setter').first()
        question_obj = Question.objects.create(
            question = question,
            creater_id = user.id,
            question_marks = data['question_marks'],
            subject_id  = user.profile_set.first().subject.id
        )#profile_set.first() it takes user profile
        question_obj.save()
        
        answer_obj = Answer.objects.create(
            answer_type  = 'TEXT',
            answer = answer,
            question_id = question_obj.id
        )
        answer_obj.save()
        serializer = QuestionSerializer(question_obj, many = False)
        return Response(serializer.data,status = status.HTTP_201_CREATED)
        
class TestPaperCreateView(CreateAPIView):
    model = TestPaper
    serializer_class = TestPaperSerializer
    
    def post(self,request,*args, **kwargs):
        data = request.data
        if 'questions' not in data:
            return Response({'message':'questions is required field'},status = status.HTTP_400_BAD_REQUEST)
        questions = data['questions'].split(",")
        number_of_questions = len(questions)
        que_obj = Question.objects.filter(id__in = questions)
        total_marks = que_obj.aggregate(total_marks = Sum('question_marks'))['total_marks']

        if 'cut_off_marks' not in data:
            return Response({'message':'cut_off_marks is required field'},status = status.HTTP_400_BAD_REQUEST)
        cut_off_marks = data['cut_off_marks']
        if int(cut_off_marks) > total_marks:
            return Response({"message": "Cut Off Marks Are greater than Total marks"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(profile__profile_choice = 'Setter' ).last()
        
        test_papaer_obj = self.model.objects.create(
            number_of_questions = number_of_questions,
            total_marks = total_marks,
            cut_off_marks  = cut_off_marks,
            setter_id = user.id,
            subject_id = user.profile_set.first().subject.id
        )
        test_papaer_obj.questions.add(*questions)
        
        test_papaer_obj.save()
        return Response(status = status.HTTP_201_CREATED)
    
class TestPaperSubmission(APIView):
    def get(self,request):
        user = User.objects.filter(profile__profile_choice='Setter').first()
        qs = TestPaper.objects.filter(is_sent_for_cheeck = False,
                                        is_checker_approved = False,
                                        is_examinar_approved = False,
                                        is_active = True,
                                        is_delete = False,
                                        setter_id = user.id)
        serializer = TestPaperSerializer(qs,many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
class TestPaperSubmissionDetails(APIView):
    def get_object(self,pk):
        return get_object_or_404(TestPaper, pk=pk)
    
    def get(self,request,pk):
        test_paper = self.get_object(pk)
        serializer = TestPaperSerializer(test_paper)
        return Response(serializer.data)
    
    def put(self,request,pk):
        test_paper = self.get_object(pk)
        serializer = TestPaperSerializer(test_paper,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message':'form is invaid'})
""" 
class CheckingTestPaperCreate(CreateAPIView):
    model = CheckingTestPaper
    tp = TestPaper.objects.filter(is_sent_for_cheeck = True,
                                        is_checker_approved = False,
                                        is_examinar_approved = False,
                                        is_active = True,
                                        is_delete = False,
)
    self.model.objects.add()
    def post(self, request,*args, **kwargs):
        params = request.data
        if 'test_paper_id' not in params:
            return Response({"message": "Test Paper is Required"}, status=status.HTTP_400_BAD_REQUEST)
        test_paper_id = params['test_paper_id']


    from django.db.models import Sum,Count,Min,Max,Avg
    
    model.objects.aggregate(Sum('population'))
    {'population__sum'   :  52366356} #aggregate return dict
    
    model.objects.aggregate(sum = Sum('population'), avg = Avg('population'))
    {'sum'   :  52366356, '
    
    
    avg':423435 }
    
    model.objects.aggregate(sum = Sum('population'))6
     {'Sum'   :  52366356}
     
     result = model.objects.aggregate(sum = Sum('population'))
     result = {'Sum'   :  52366356}
     result['Sum'] = 52366356
     
"""