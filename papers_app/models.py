from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Subject(models.Model):
    """
    SUbject Name
    """
    subject_name = models.CharField(max_length=64)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.subject_name

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_role_choice =(('Setter','Setter'),('Checker' ,'Checker'),('Examinar','Examinar')) 
    profile_choice = models.CharField(max_length=10, choices = user_role_choice)
    subject  = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True,
    blank=True)
    mobile_number = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.user.username} - profile"



class Question(models.Model):
    """
    Question For now i have given normal text Question
    if required we can add Multiple choise questions also
    if we delete subject then all related Questions and answers also deleted
    Question marks means Just how many marks this question will contains
    suppose 5 marks or 10 marks like this
    """
    question = models.CharField(max_length=256)
    creater = models.ForeignKey(User, on_delete=models.CASCADE)
    question_marks = models.IntegerField(default=0)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.question}-{self.subject}-{self.question_marks}"

class Answer(models.Model):
    
    """
    Answer For Question For now i have added Only text base answer
    For this if you guys want add image answer or mutliple choises also
    """

    Answer_type = (('TEXT','text_type'),('IMAGE','image_type'),('AUDIO','audio_type'))
    answer_type = models.CharField(max_length=10,choices = Answer_type, blank=True, null=True)
    answer = models.TextField()
    question = models.ForeignKey(Question,  on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Answer is for {self.question}"


class TestPaper(models.Model):
    """
    num_of_questions = total nuber of questions contains by this paper
    questions = One question can be in number of papers and one paper contains many questions
    total_marks = marks for this paper
    subject = for which subject belongs to this paper 
            if subject deleted then Test paper also be deleted
    setter = He is Lecturer
            if he is removed then Test paper also be deleted
    checker = 
    examiner 
    checker_review
    examiner review
    is_approved = Is finally paper approved or not
    """
    number_of_questions = models.IntegerField()
    questions = models.ManyToManyField(Question, default=[])
    total_marks = models.IntegerField()
    cut_off_marks =models.PositiveIntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    setter = models.ForeignKey(User, on_delete=models.CASCADE,
                            related_name="set_papers")
    checker = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                            related_name="checked_papers",
                            blank=True,
                            null=True)
    examiner = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                            related_name="examined_papers",
                            blank=True,
                            null=True)
    checker_review = models.TextField(blank=True,
                            null=True)
    examiner_review = models.TextField(blank=True,
                            null=True)
    is_sent_for_cheeck = models.BooleanField(default=False)
    is_checker_approved = models.BooleanField(default=False)
    is_examinar_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default = True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)
    
    # def __str__(self):
    #     return 'test_paper '

class CheckingTestPaper(models.Model):
    test_paper = models.ForeignKey(TestPaper,related_name = 'test_check', on_delete= models.CASCADE)
    checker_review = models.TextField(blank=True,
                            null=True)
    is_checker_approved = models.BooleanField(default=False)

class ApprovedTestPaper(models.Model):
    test_paper = models.ForeignKey(TestPaper,related_name = 'test_approve',on_delete= models.CASCADE)
    examiner_review = models.TextField(blank=True,
                            null=True)
    is_examiner_approved = models.BooleanField(default=False)