# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.conf import settings
from django.db.models import Max, Sum
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm


from tedbot.forms import ReturnAnswer
from tedbot.models import Question, Answer, Course, Tour, Mail, Admission, Unable, Log, Schedule

from random import *

#from wordsegment import load, segment
from nltk.corpus import stopwords
from nltk import word_tokenize
import nltk, string, os, re 

from tedbot.inputclassify import *
from tedbot.sentsimilar_jac import *
#from tedbot.sentsimilar import *
#from tedbot.sentsimilar_vec import *

sno = nltk.stem.SnowballStemmer('english')

x  = classifier()
thread = ["Let's get started"]
state = "general"
chatmail = "sum mail"
q = 0 
highest = 0
year = "one" 
count = 1

def remove_stop_words(sentence):
	stop_words = set(stopwords.words('english'))
	word_tokens = word_tokenize(sentence)
	filtered = [w for w in word_tokens if not w in stop_words]

	sent = ""
	sent = "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in filtered]).strip()
	return sent
def remove_stop(sentence):
	stripped = remove_stop_words(sentence)
	if len(word_tokenize(stripped)) < 2:
		stripped = stripped + " are" +" you"
	return stripped
def findWholeWord(w): 
	return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def checkpos(text):
	if findWholeWord('yes')(text) or findWholeWord('yeah')(text) or findWholeWord('okay')(text) or findWholeWord('accept')(text) or findWholeWord('agree')(text) or findWholeWord('fantastic')(text)or findWholeWord('perfect')(text) or findWholeWord('good')(text) or findWholeWord('great')(text) or findWholeWord('yea')(text) or findWholeWord('affirmative')(text) or findWholeWord('by all means')(text) or findWholeWord('very well')(text) or findWholeWord('yup')(text) or findWholeWord('sure')(text) or findWholeWord('totally')(text) or findWholeWord('ok')(text):
		return True
	else:
		return False 

def checkneg(text):
	if findWholeWord('No')(text) or findWholeWord('nope')(text) or findWholeWord('refuse')(text) or findWholeWord('disagree')(text) or findWholeWord('no way')(text) or findWholeWord('negative')(text) or findWholeWord('not')(text) or findWholeWord('nuh')(text):
		return True
	else:
		return False
def stematize(sentence):

	stemmed = []
	filtered = word_tokenize(sentence)
	for w in filtered:
		stemmed.append(sno.stem(w))

	sent = "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in stemmed]).strip()

	return sent
def returnanswer(question):
	y = []
	global highest
	highest = 0
	global q
	global state
	q = 0
	answer = "._."
	course = "."
	requirements = "."
	question_id = 1
	tally = 1

	other = ["I'm not sure I get you.", "Come Again?", "I don't follow", "Can you please clarify?", "I'm sorry, what was that?"]
	greet = ["Hello there, I'm Tedbot", "Hey", "Hey, I'm Tedbot", "Hello", "Hi"]
	statement = ["I see...", "Mkay", "Anythin else, just ask", "Cool, cool, cool", "You seem to know what you are talking about"]
	continuer = ["Yeah", "That's how it is", "Moving on, what do you want to know?", "I hope I can be helpful", "I do hope you enjoy Elimu University"]
	accept = ["Happy to help", "Anything else you want to know, you know where to find me", "Okay, then", "So tell your friends to ask Tedbot for help.", "Good"]
	emotion = ["If that's how you feel...*shrugs", "I see...", "As a Bot, I'm not sure what to say.", "You'll be Okay", "*not sure what to do about that."]
	reject = ["That's how it is", "You don't agree?", "You'll have to trust me on this.", "Okay,then. Just ask me something else", "I see we have a know it all here"]
	bye = ["See ya!", "Gerrarahia then, I have other requests", "Bye", "It was fun chatting with you", "Hope I was helpful"]
	clarify = ["How about you get more information from the school website", "That's really it", "You can get more help from the admissions desk", "Ask me again maybe I can get a better answer", "That's thebest answer I can get you"]

	y = x.classify_many(dialogue_act_features(question)) 

	if y[0] == 4 or y[0] == 1 or y[0] == 11 or question[0:3] == 'Can' or question[0:3] == 'can' or question[0:2] == 'Do' or question[0:2] == 'do' or question[0:4] == 'Will' or question[0:4] == 'will':
		if len(word_tokenize(question)) < 3 or len(question) < 2: 
			answer = other[randint(0, 4)]
		else:			
			for entry in Question.objects.values_list('entry', flat=True).all():
				e = entry.encode('ascii', 'ignore')
				if symmetric_sentence_similarity(question, e) > highest:
					highest = symmetric_sentence_similarity(question, e) 
			if highest < 0.01:
				answer = "I'm not sure I can help you with that...Would you like to email student services?"
				state = "help"
				t = Unable.objects.create(entry=question)
				t.save()
			else:
				for entry in Question.objects.values_list('entry', flat=True).all():
					e = entry.encode('ascii', 'ignore')
					if symmetric_sentence_similarity(question, e) == highest:
						q = Question.objects.get(entry=e).pk
						try: 
							answer = Answer.objects.get(question_id=q).answer
							tally = Answer.objects.get(question_id=q).tally
							tally += 1 
							t = Answer.objects.get(question_id=q)
							t.tally = tally
							t.save()
						except:
							answer = "I'm not sure I can help you with that...Would you like to email student services?"
							state = "help" 
						#New code
						arr = [11, 12, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29]
						arr_two = [78, 79, 80, 81, 93, 94, 44]
						arr_three = [101, 102, 103, 104] 
						arr_four = [5, 6, 105, 106]
						arr_five = [107, 108, 109, 110]
						if q in arr:
							state = "course" 
						if q in arr_two:
							state = "tour" 
						if q in arr_three:
							state = "help"
						if q in arr_four:
							state = "admissions"
						if q in arr_five:
							state = "schedule"

	elif y[0] == 0:
		answer = emotion[randint(0, 4)] 
	elif y[0] == 6:
		answer = accept[randint(0, 4)]  
	elif y[0] == 7: 
		answer = clarify[randint(0, 4)]
	elif y[0] == 8:
		answer = statement[randint(0, 4)]
	elif y[0] == 9:
		answer = reject[randint(0, 4)]
	elif y[0] == 10:
		answer = greet[randint(0, 4)]
	elif y[0] == 11:
		answer = statement[randint(0, 4)]
	elif y[0] == 12:
		answer = reject[randint(0, 4)]
	elif y[0] == 14:
		answer = other[randint(0, 4)]
	elif y[0] == 13:
		answer = bye[randint(0, 4)]

	return answer
  

def returncourse(question):
	try:
		answer = Course.objects.filter(course__search=question)[0].entryrequirements
	except:
		answer = "I could not find that course please check the university website for more information on courses"
	try:
		tally = Course.objects.filter(course__search=question)[0].tally
		tally += 1 
		t = Course.objects.filter(course__search=question)[0]
		t.tally = tally
		t.save() 
	except:
		None 
	global state
	state = "general"
	return answer

def returntour(question):
	global state
	if checkpos(question) and not checkneg(question):
		answer = "Could you give me your email address, please? Then I can register you for a tour"
		state = "mail_tour"
	elif checkneg(question) and not checkpos(question):
		answer = "Okay but you can register for a tour at any time on the university website"
		state = "general"
	else:
		answer = "I didn't quite get that. Please re-ask your question."
		state = "general" 
	return answer 

def returnmail(text):
	global state
	match = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
	if not match:
		answer = "I did not quite get your email address. Could you try that again?"
	else:
		mail = match[0]
		t = Tour.objects.create(email=mail)
		t.save()
		answer = match[0] + " has been saved.You have been registered to attend a tour to the University on one of the following dates. 6/Aug/2018, 13/Aug/2018, 27/Aug/2018, 3/Sept/2018, 10/Sept/2018, 17/Sept/2018. The tour will last for 2 or so hours and will take you around the university facilities."
		state = "general"
	return answer 

def returnhelp(question):
	global state
	if checkpos(question) and not checkneg(question):
		answer = "Could you give me your email address, please?"
		state = "mail_help"
	elif checkneg(question) and not checkpos(question):
		answer = "Okay but you can contact student services any time you like. Their email address is help@elimu.ac.ke"
		state = "general"
	else:
		answer = "I didn't quite get that. Please re-ask your question."
		state = "general"
	return answer

def returnhelp_mail(text):
	global state
	global chatmail
	match = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
	if not match:
		answer = "I did not quite get your email address. Could you try that again?"
	else:
		chatmail = match[0]
		mail = match[0]
		t = Mail.objects.create(email=mail)
		t.save()
		answer = match[0] + " has been saved. Type up your query to student student services and I will send it for you"
		state = "mail_body"
	return answer

def returnhelp_body(question):
	global state
	global chatmail
	t = Mail.objects.get(email=chatmail)
	t.body = question
	t.save()
	answer = "Your message has been sent. Student services will get back to you in one or two working days depending on the number of responses they have to respond to."
	

	state = "general"
	return answer

def returnadmissions(text):
	global state
	if checkpos(text) and not checkneg(text):
		answer = "Please give me this number"
		state = "admissions_status"
	elif checkneg(text) and not checkpos(text):
		answer = "Don't worry about it, when you filled an application form you included your email address, check it and then get back to me later"
		state = "general"
	else:
		answer = "I didn't quite get that, sorry. Please try again laterPlease re-ask your question."
	return answer

def returnadmissions_status(question):
	global state
	try:
		answer = Admission.objects.get(admissionref=question).status
		if answer == "Complete":
			answer = "Your application form has been completed, please check your email for further instructions from the admissions team"
			state = "general"
		else:
			answer = "Your application has still not been processed completely. Please check again at a later time or await for an email from the admissions team."
			state = "general" 
	except:
		answer = "I seem to have encountered a problem fetching your reference number. Could you please checkit again and try again later"
		state = "general"
	return answer

def returnschedule(question):
	global state
	if checkpos(question) and not checkneg(question):
		answer = "Okay, so what is the unit code?"
		state = "schedule_code"
	elif checkneg(question) and not checkpos(question):
		answer = "That's okay, you should get your timetable on your university mail"
		state = "general"
	else:
		answer = "I didn't quite get that. Please re-ask your question."
		state = "general"
	return answer

def returnschedule_code(text):
	global state
	match = re.findall(r'[\w\.-]+/\w+', text)
	code = match[0]
	if not match:
		answer = "I did not quite get that course code, retype it as com/300"
		state = "schedule_code"
	else:
		try:
			answer = Schedule.objects.filter(course__search=code)[0].schedule
		except:
			answer = "I could not find that unit but that's okay, you should get your timetable on your university e-mail, remember the format is as com/300"
		state = "general"
	return answer

# Create your views here. 
def index(request):
	global count
	userchat = "."
	answerchat = "." 
	if request.method == 'POST': 
		myform = ReturnAnswer(request.POST)
		if myform.is_valid():
			userchat = myform.cleaned_data['question']
			thread.append(userchat)
			if state == "general":
				answerchat = returnanswer(userchat)	
			elif state == "course":
				if len(word_tokenize(userchat)) > 2:
					answerchat = "I did not quite get that, please resend that using two words or less so I can check the database quicker, it's a lot to courses on the database, you know. ;-)"
				else:
					answerchat = returncourse(userchat) 
			elif state == "tour":
				answerchat = returntour(userchat)
			elif state == "mail_tour":
				answerchat = returnmail(userchat)
			elif state == "help":
				answerchat = returnhelp(userchat) 
			elif state == "mail_help":
				answerchat = returnhelp_mail(userchat)
			elif state == "mail_body":
				answerchat = returnhelp_body(userchat)
			elif state == "admissions":
				answerchat = returnadmissions(userchat)
			elif state == "admissions_status":
				if len(word_tokenize(userchat)) > 1:
					answerchat = "Whoops! I did not quite get that, please resend your refence number only, no other text. (Makes it easier for me to look it up in the database for you) ;-)"
				else:
					answerchat = returnadmissions_status(userchat)
			elif state == "schedule":
				answerchat = returnschedule(userchat)
			elif state == "schedule_code":
				answerchat = returnschedule_code(userchat)

			t = Log.objects.create(entry=userchat, response=answerchat)
			t.save() 
			thread.append(answerchat) 
			
			
 
	else:
		myform = ReturnAnswer()
	return  render(request, 'tedbot/index.html', {"answer": userchat, "question": userchat, "thread": thread, "ID": q, "state": state, "score": highest})



def chatanalytics(request):
	high_tally = Course.objects.all().aggregate(Max('tally'))['tally__max']
	tally_course = Course.objects.filter(tally=high_tally)[0].course
	query_tally = Answer.objects.all().aggregate(Max('tally'))['tally__max']
	query_about = Answer.objects.filter(tally=query_tally)[0].about

	total_course = Course.objects.aggregate(Sum('tally'))['tally__sum']
	total_query = Answer.objects.aggregate(Sum('tally'))['tally__sum']
	total_tour = Tour.objects.all().count()
	total_help = Mail.objects.all().count() 

	total_application = Answer.objects.filter(about="Application").aggregate(Sum('tally'))['tally__sum']
	total_schedule = Answer.objects.filter(about="Student Class Schedule").aggregate(Sum('tally'))['tally__sum']
	total_admission = Answer.objects.filter(about="Admission").aggregate(Sum('tally'))['tally__sum']
	total_chat = Answer.objects.filter(about="chat").aggregate(Sum('tally'))['tally__sum']
	total_entry = Answer.objects.filter(about="Entry Requirements").aggregate(Sum('tally'))['tally__sum']
	total_defer = Answer.objects.filter(about="Deferred Studies").aggregate(Sum('tally'))['tally__sum']
	total_residence = Answer.objects.filter(about="Residence").aggregate(Sum('tally'))['tally__sum']
	total_tours = Answer.objects.filter(about="Tour").aggregate(Sum('tally'))['tally__sum']
	total_fees = Answer.objects.filter(about="School Fees").aggregate(Sum('tally'))['tally__sum']
	total_aid = Answer.objects.filter(about="Financial Aid").aggregate(Sum('tally'))['tally__sum']
	total_sports = Answer.objects.filter(about="Sports").aggregate(Sum('tally'))['tally__sum']

	return render(request, 'tedbot/chatanalytics.html', {"total_sports": total_sports,"total_aid": total_aid,"total_fees": total_fees,"total_tours": total_tours,"total_residence": total_residence, "total_defer": total_defer, "total_entry": total_entry, "total_chat": total_chat, "total_application": total_application, "total_schedule": total_schedule, "total_admission": total_admission, "total_tour": total_tour, "total_help": total_help, "total_course": total_course, "total_query": total_query, "course_enquired": tally_course, "course_tally": high_tally, "query_tally": query_tally, "query_about": query_about})
 
#, "query_about": query_about {{ query_about }} 
def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/')
	else:
		form = UserCreationForm()
	return render(request, 'signup.html', {'form': form})
 

def pagelogout(request):
	if request.method == "POST":
		logout(request)

	return  render(request, 'logout.html',)

def elimuhome(request):
	return render(request, 'tedbot/elimuhome.html',)

def housing(request):
	return render(request, 'tedbot/housing.html',)

def scholarships(request):
	return render(request, 'tedbot/scholarships.html',)
