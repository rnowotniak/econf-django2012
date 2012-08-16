# -*- coding: utf-8 -*-


from django.contrib.auth.models import User
from django.contrib.formtools.preview import FormPreview
from django import forms
from django.forms import widgets
from django.forms.models import ModelForm
from django.template.response import TemplateResponse
from confapp.models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        #fields = ('first_name', 'last_name')
        exclude = ('user', )
        widgets = {
            'payment': widgets.RadioSelect()
        }

    first_name = forms.CharField(label=u'Imię', max_length=30)
    last_name = forms.CharField(label='Nazwisko', max_length=30)
    email = forms.EmailField()
    #payment = forms.ChoiceField(widget=forms.RadioSelect())

    required_css_class = "required"
    error_css_class = "error"

    def __init__(self, *args, **kw):
        super(ProfileForm, self).__init__(*args, **kw)
        self.requser = None
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
            if not data == self.requser.email:
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
        if self.requser:
            # profile update
            profile.user.first_name=self.cleaned_data['first_name']
            profile.user.last_name=self.cleaned_data['last_name']
            profile.user.username=self.cleaned_data['email']
            profile.user.email=self.cleaned_data['email']
            profile.user.save()
            profile.save()
            return profile
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


class ProfileFormPreview(FormPreview):
#    preview_template = 'formtools/preview.html'
    form_template = 'registration/form.html'

    def done(self, req, cleaned_data):
        form = ProfileForm(req.POST)
        form.save()
        # TODO send mail
        return TemplateResponse(req, "thanks.html")


