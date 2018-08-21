# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Question(models.Model):
	entry = models.CharField(max_length=200)

	def __str__(self):
		return self.entry

class Answer(models.Model):
	question = models.ForeignKey(Question)
	answer = models.CharField(max_length = 600)
	about = models.CharField(max_length= 100, default="chat") 
	tally = models.IntegerField(default=0)

	def __str__(self):
		return self.answer

class Course(models.Model):
	course = models.CharField(max_length=200)
	entryrequirements = models.CharField(max_length=1500)
	tally = models.IntegerField(default=0)

	def __str__(self):
		return self.course

class Tour(models.Model):
	email = models.CharField(max_length=150)
	created = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)

	def __str__(self):
		return self.email
 
class Mail(models.Model):
	email = models.CharField(max_length=150)
	subject = models.CharField(max_length=50, default="Chatbot user assistance")
	body = models.CharField(max_length=300)

	def __str__(self):
		return self.body

class Admission(models.Model):
	admissionref = models.CharField(max_length=100)
	status = models.CharField(max_length=100)

	def __str__(self):
		return self.status

class Unable(models.Model):
	entry = models.CharField(max_length=100)
	created = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)

	def __str__(self):
		return self.entry

class Log(models.Model):
	entry = models.CharField(max_length=200)
	response = models.CharField(max_length=600)
	created = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False) 

	def __str__(self):
		return self.entry 

class Schedule(models.Model):
	course = models.CharField(max_length=50)
	schedule = models.CharField(max_length=100)

	def __str__(self):
		return self.course 