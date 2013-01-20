import re
from django.contrib.auth.models import User
from django import forms
from django.core.files.images import get_image_dimensions
from events.models import UserProfile, AccomplishedEvent

class RegistrationForm(forms.Form):
    username = forms.CharField(label=u'Username', max_length=30)
    email = forms.EmailField(label=u'Email')
    password1 = forms.CharField(
            label=u'Password',
            widget=forms.PasswordInput()
            )
    password2 = forms.CharField(
            label=u'Password (Again)',
            widget=forms.PasswordInput()
            )

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
          raise forms.ValidationError('Username can only contain '
              'alphanumeric characters and the underscore.')
        try:
          User.objects.get(username=username)
        except User.DoesNotExist:
          return username
        raise forms.ValidationError('Username is already taken.')



class EventSaveForm(forms.Form):
    
    title = forms.CharField(
            label=u'Title',
            widget=forms.TextInput(attrs={'size': 64})
            )
    
    description = forms.CharField(
            label=u'Description',
            widget = forms.Textarea(attrs={'size': 150})
            )
    
    tags = forms.CharField(
            label=u'Tags',
            required=False,
            widget=forms.TextInput(attrs={'size': 64})
            )
    
    share = forms.BooleanField(
            label=u'Share on the main page',
            required=False
            )      

class SearchForm(forms.Form):
        query = forms.CharField(
        label=u'Enter a title to search for',
        widget=forms.TextInput(attrs={'size': 32})
        )


class UserProfileForm(forms.Form):

    firstName = forms.CharField(
            label=u'First Name',
            widget=forms.TextInput(attrs={'size': 64})
            )

    lastName = forms.CharField(
            label=u'Last Name',
            widget=forms.TextInput(attrs={'size': 64})
            )

    tagline = forms.CharField(
            label=u'Describe Yourself in One Line',
            max_length = 100,
            widget = forms.Textarea
            )

    





