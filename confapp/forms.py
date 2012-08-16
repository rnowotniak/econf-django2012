# -*- coding: utf-8 -*-
import django

from django.contrib.auth.models import User
from django.contrib.formtools.preview import FormPreview
from django import forms
from django.core.mail import send_mail
from django.forms import widgets
from django.forms.models import ModelForm
from django.template import Context
from django.template.response import TemplateResponse
import smtplib
from confapp.models import Account, Paper
from django.conf import settings

class AccountForm(ModelForm):
    class Meta:
        model = Account
        #fields = ('first_name', 'last_name')
        exclude = ('user', )
        widgets = {
            'accounttype': widgets.RadioSelect()
        }

    first_name = forms.CharField(label=u'Imię', max_length=30)
    last_name = forms.CharField(label='Nazwisko', max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget = widgets.PasswordInput(), label='Hasło')
    password2 = forms.CharField(widget = widgets.PasswordInput(), label='Powtórz hasło')

    required_css_class = "required"
    error_css_class = "error"

    def __init__(self, *args, **kw):
        super(AccountForm, self).__init__(*args, **kw)
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
            'accounttype',
            'phone',
            'address2'
        ]

    def clean_password(self):
        if len(self.cleaned_data['password']) < 6:
            raise forms.ValidationError('Podaj hasło co najmniej 6-znakowe')
        return self.cleaned_data['password']

    def clean(self):
        cleaned_data = super(AccountForm, self).clean()
#        print cleaned_data
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                raise forms.ValidationError('Podałeś różne hasła')
        return cleaned_data

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            User.objects.get(email=data)
            if not self.requser or not data == self.requser.email:
                raise forms.ValidationError('W systemie jest już zarejestrowany taki adres e-mail')
        except User.DoesNotExist:
            pass
        return data


    #	def clean(self):
    #		cleaned_data = super(AccountForm, self).clean()
    #		try:
    #			User.objects.get(email = cleaned_data['email'])
    #			self._errors['email'] = self.error_class(['Jest taki user'])
    #			del cleaned_data['email']
    #		finally:
    #			return cleaned_data


    def save(self, commit = True):
        account = super(AccountForm, self).save(commit=False)
        if self.requser: # TODO zrobic to lepiej, czytelniej
            # account update
            account.user.first_name=self.cleaned_data['first_name']
            account.user.last_name=self.cleaned_data['last_name']
            account.user.username=self.cleaned_data['email']
            account.user.email=self.cleaned_data['email']
            account.user.save()
            account.save()
            return account
        user = User(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'])
#        print "Ustawiam haslo: %s" % self.cleaned_data['password']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Caution! Account objects is created automatically, due to User signal!
            account.id = user.account.id
            account.user = user
            account.save()
#            print account
        else:
            account.user = user
            user.account = account
        user.cleartext = self.cleaned_data['password'] # required to send the mail with confirmation
        return account


class AccountFormPreview(FormPreview):
#    preview_template = 'formtools/preview.html'
    form_template = 'registration/form.html'

    def process_preview(self, request, form, context):
#        print dir(context['form'].fields['accounttype'].widget)
        context['accounttype'] = form.instance.accounttype.name

    def done(self, req, cleaned_data):
        form = AccountForm(req.POST)

        account = form.save(commit = True)
        try:
            t = django.template.loader.get_template('registration/mail.txt')
            c = Context({'user': account.user})
            body = t.render(c)
#            print body
            send_mail('Forum Innowacji Młodych Badaczy -- potwierdzenie rejestracji',
                body, settings.EMAIL_HOST_USER, [cleaned_data['email']])
            return TemplateResponse(req, "thanks.html")
        except smtplib.SMTPException, e:
            print e
            return TemplateResponse(req, "thanks.html", {'mailerror':True})


class ContactForm(forms.Form):
    message = forms.CharField(widget = widgets.Textarea(), label='Treść wiadomości')
    sendcopy = forms.BooleanField(initial = True, required = False)

class PaperForm(ModelForm):
    class Meta:
        model = Paper
#        exclude = ('user', )
#        fields = ('first_name', 'last_name')

    required_css_class = "required"
    error_css_class = "error"