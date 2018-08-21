# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from tedbot.models import Question, Answer, Course, Tour, Mail, Admission, Unable, Log, Schedule
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
	list_display = ('pk', 'entry')
	list_display_links = ('entry',)

class AnswerAdmin(admin.ModelAdmin):
	list_display = ('question_id', 'question', 'answer', 'about', 'tally')
	list_display_links = ('answer',)

class CourseAdmin(admin.ModelAdmin):
	list_display = ('course', 'entryrequirements', 'tally')
	list_display_links = ('course',)

class TourAdmin(admin.ModelAdmin):
	list_display = ('email', 'created')

class MailAdmin(admin.ModelAdmin):
	list_display = ('email', 'subject', 'body')

class AdmissionAdmin(admin.ModelAdmin):
	list_display = ('admissionref', 'status')

class UnableAdmin(admin.ModelAdmin):
	list_display = ('entry', 'created')

class LogAdmin(admin.ModelAdmin):
	list_display = ('entry', 'response', 'created')

class ScheduleAdmin(admin.ModelAdmin):
	list_display = ('course', 'schedule')
	list_display_links = ('schedule',)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Course, CourseAdmin) 
admin.site.register(Tour, TourAdmin)
admin.site.register(Mail, MailAdmin)
admin.site.register(Admission, AdmissionAdmin)
admin.site.register(Unable, UnableAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(Schedule, ScheduleAdmin)