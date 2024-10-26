from django import forms

class UserRegistration(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(max_length=100)


class Homeform(forms.Form):
    username=forms.CharField(max_length=100,label="Enter Username")
    groupname=forms.CharField(max_length=100)
    password=forms.CharField(max_length=100,label="Enter Password")

