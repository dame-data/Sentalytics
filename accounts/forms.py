from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
		UserCreationForm
	)

from django.forms import ModelForm, Textarea,HiddenInput
from accounts.models import FileUploads

class AddUsersForm(UserCreationForm):
	email = forms.EmailField(required = False)
	class Meta:
		model = User
		fields = (
			'username',
			'email',
			'password1',
			'password2'
			)

	def save(self,commit = False):
		user = super(AddUsersForm, self).save(commit=False)
		user.email = self.cleaned_data['email']

		if commit:
			user.save()

		return user

class UploadFileForm(forms.ModelForm):
	class Meta:
		model = FileUploads
		fields = (
			'title',
			'file',
			'summary'
			)
		widgets = {
			'summary':Textarea(attrs={"class":"materialize_textarea","data-length":"150"}),
		}