from django import forms

class ReturnAnswer(forms.Form):
	question = forms.CharField(max_length=200)