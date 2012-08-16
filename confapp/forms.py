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
    password = forms.CharField(widget = widgets.PasswordInput(), label='Hasło')
    password2 = forms.CharField(widget = widgets.PasswordInput(), label='Powtórz hasło')

    required_css_class = "required"
    error_css_class = "error"

    def __init__(self, *args, **kw):
        super(ProfileForm, self).__init__(*args, **kw)
        self.requser = None
        self.fields.keyOrder = [
            'first_name',
            'last_name',
            'email',
            'password',
            'password2',
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

    def clean_password(self):
        if len(self.cleaned_data['password']) < 6:
            raise forms.ValidationError('Podaj hasło co najmniej 6-znakowe')
        return self.cleaned_data['password']

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
#        print cleaned_data
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                raise forms.ValidationError('Podałeś różne hasła')
        return cleaned_data

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
        print "Ustawiam haslo: %s" % self.cleaned_data['password']
        user.set_password(self.cleaned_data['password'])
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

    def process_preview(self, request, form, context):
#        print dir(context['form'].fields['payment'].widget)
        context['payment'] = form.instance.payment.name

    def done(self, req, cleaned_data):
        form = ProfileForm(req.POST)
#        print form.fields
        form.save()
        # TODO send mail
        return TemplateResponse(req, "thanks.html")


