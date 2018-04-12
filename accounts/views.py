from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from accounts.forms import (
	AddUsersForm,
	UploadFileForm
	)
from django.contrib.auth import authenticate,login,update_session_auth_hash,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import FileUploads


# importing the NLP toolkits
import os
from nltk.tokenize import (
		sent_tokenize,
		word_tokenize
	)
from nltk import pos_tag
from nltk.corpus import stopwords
from textalyzer import Textalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Create your views here.

@login_required
def login_auth(request):
	username = request.POST['username']
	password = request.POST['password1']
	user = authenticate(username = username, password = password)
	if user is not None and user.is_authenticated:
		login(request,user)
		return redirect('accounts/dashboard.html')

def registration(request):
	if request.method == 'POST':
	    form = AddUsersForm(request.POST)
	    if form.is_valid():
	    	instance = form.save(commit=False)
	    	instance.save()
	    	username = form.cleaned_data.get("username")
	    	raw_password = form.cleaned_data.get("password1")
	    	user = authenticate(username=username, password=raw_password)
	    	login(request, user)
	    	return redirect('/accounts')
	else:
		form = AddUsersForm()
		context = {
			'form':form
		}
		return render(request, 'accounts/register.html',context)
   


@login_required
def dashboard(request):
	context = {
		'form':"banks"
	}
	return render(request,'accounts/dashboard.html',context)


@login_required
def sentiment(request,primary_id):
	if request.method == 'POST':
		form = UploadFileForm(request.POST or None, request.FILES or None)
		get_id = primary_id
		if form.is_valid():
			content = request.FILES['file']
			if content.multiple_chunks():
				print("Uploaded file is too big (%.2f MB)" % (content.size/(1000*1000),))
			
			file_data = content.read()
			instance = form.save(commit=False)
			instance.user_id = get_id
			instance.content = file_data
			instance.save()
			return redirect('/accounts')
	else:
		form = UploadFileForm()
		context = {
			'upload_form':form
		}
		return render(request,'accounts/sentiment_form.html',context)

@login_required
def attachments(request,primary_id):
	all_attachments = FileUploads.objects.filter(user_id=primary_id)
	all_att_counts = all_attachments.count()
	
	context = {
		'counts':all_att_counts,
		'all_attachments':all_attachments
	}
	return render(request,'accounts/attachments.html',context)

@login_required
def data_processing(request,primary_id):
	file_content = ''
	get_attachment = FileUploads.objects.get(id=primary_id)
	file_data = get_attachment.content

	# Tokenization starts here
	sentence = sent_tokenize(file_data)
	words = word_tokenize(str(sentence))

	#Removing punctuation and other stuff
	punct_free = [word for word in words if word.isalpha()]
	stop_words = [word for word in punct_free if word not in stopwords.words('english')]

	# Processing starts from here
	replacers = Textalyzer.RegexpReplacer()

	# removing unwanted data
	stripped_data = replacers.replace(str(stop_words))
	# This is the fun part
	sid = SentimentIntensityAnalyzer()
	sdata = sid.polarity_scores(stripped_data)

	positivity = sdata['pos']
	negativity = sdata['neg']
	neutrality = sdata['neu']

	compound   = sdata['compound']
	
	context = {
		"positivity":positivity,
		"negativity":negativity,
		"neutrality":neutrality,
		"compound":compound
	}
	return render(request,'accounts/results.html',context)