from django import forms
# -*- coding: utf-8 -*-



class DocumentForm(forms.Form):
    """Image upload form."""
    avatar = forms.ImageField()
    
class ThreadForm(forms.Form):
	Title = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
	Description = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'placeholder': 'Description'}))
	Topic = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Topic'}))

class CommentForm(forms.Form):
	Description = forms.CharField(max_length=1000)
	Thread = forms.IntegerField()

class UserVideoForm(forms.Form):
	video = forms.FileField() 

#class UploadFileForm(forms.Form):
#    title = forms.CharField(max_length=100)
#    file = forms.ImageField()