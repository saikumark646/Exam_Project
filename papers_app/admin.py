from django.contrib import admin

from .models import *



admin.site.register(Subject)
admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(TestPaper)
admin.site.register(CheckingTestPaper)
admin.site.register(ApprovedTestPaper)

