# -*- coding: utf-8 -*-

# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from models import Profile
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.db import transaction
from django.template.response import TemplateResponse

def main(req):
    users = Profile.objects.all()
    return TemplateResponse(req, "main.html", {"users": users})
    #return render_to_response('main.html', {'users': users})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        #fields = ('first_name', 'last_name')
        exclude = ('user', )
        widgets = {
            'payment': forms.RadioSelect()
        }

    first_name = forms.CharField(label=u'Imię', max_length=30)
    last_name = forms.CharField(label='Nazwisko', max_length=30)
    email = forms.EmailField()
    #payment = forms.ChoiceField(widget=forms.RadioSelect())

    required_css_class = "required"
    error_css_class = "error"

    def __init__(self, *args, **kw):
        super(ProfileForm, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'first_name',
            'last_name',
            'email',
            'organization',
            'institute',
            'address',
            'postcode',
            'city',
            'nip',
            'payment',
            'phone',
            'address2'
        ]

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            User.objects.get(email=data)
            raise forms.ValidationError('jest user')
        except User.DoesNotExist:
            pass
        return data


    #	def clean(self):
    #		cleaned_data = super(ProfileForm, self).clean()
    #		try:
    #			User.objects.get(email = cleaned_data['email'])
    #			self._errors['email'] = self.error_class(['Jest taki user'])
    #			del cleaned_data['email']
    #		finally:
    #			return cleaned_data


    def save(self, commit = True):
        profile = super(ProfileForm, self).save(commit=False)
        user = User(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'])
        user.set_password('abc1')
        if commit:
            user.save()
            profile.id = user.profile.id
            profile.user = user
            profile.save()
            print profile
        return profile


def register(req):
    form = ProfileForm()
    if req.method == 'POST':
        form = ProfileForm(req.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('ok!')
        else:
            # XXX
            pass
    return TemplateResponse(req, "register.html", {"form": form})
