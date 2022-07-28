from django.urls import path
from .views import ProfileCreation,ProfileDetail,SubjectList,QueationCreateView,TestPaperCreateView ,TestPaperSubmission,TestPaperSubmissionDetails
app_name = 'papers_app'

urlpatterns = [
    path('register/',ProfileCreation.as_view(),name = 'registraction'),
    path('register/<int:pk>/',ProfileDetail.as_view(),name = 'profile_details'),
    path('subject/',SubjectList.as_view(),name = 'subject_list'),
    path('question/',QueationCreateView.as_view(),name = 'question_list'),
    #path('question/<int:pk>/',QueationDetailCreateView.as_view(),name = 'QueationDetailCreateView')
    path('testpaper/',TestPaperCreateView.as_view(),name = 'test_paper'),
    path('testpapersub/',TestPaperSubmission.as_view(),name = 'test_sub'),
    path('testpapersub/<int:pk>/',TestPaperSubmissionDetails.as_view(),name = 'test_sub_details')
]