# -*- coding: utf-8 -*-

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from models import Profile
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.template.response import TemplateResponse

def main(req):
    print req.user
    if req.user.is_authenticated():
        return TemplateResponse(req, "panel.html")
    users = Profile.objects.all()
    return TemplateResponse(req, "base.html", {"users": users})
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


#def register(req):
#    form = ProfileForm()
#    if req.method == 'POST':
#        form = ProfileForm(req.POST)
#        if form.is_valid():
#            form.save()
#            return HttpResponse('ok!')
#        else:
#            # XXX
#            pass
#    return TemplateResponse(req, "register.html", {"form": form})

#def login(req):
#    state = ''
#    username = ''
#    if req.POST:
#        username = req.POST['username']
#        user = authenticate(username = username, password = req.POST['password'])
#        if user and user.is_active:
#            state = 'ok'
#            DjangoLogin(req, user)
#            return redirect('/')
#        else:
#            state = 'zle logowanie'
#    return TemplateResponse(req, "login.html", {'state':state,'username': username})

#def logout(req):
#    DjangoLogout(req)
#    return redirect('/')

#@login_required
#def changepass(req):
#    msg = ''
#    if req.POST:
#        if req.user.check_password(req.POST['oldpass']):
#            msg = 'dobre stare haslo'
#            if req.POST['pass1'] != req.POST['pass2']:
#                msg = 'różne nowe hasła'
#            elif len(req.POST['pass1']) < 3:
#                msg = 'za krótkie nowe hasło'
#            else:
#                # all ok
#                req.user.set_password(req.POST['pass1'])
#                req.user.save()
#                msg = 'Hasło zmienione'
#        else:
#            msg = 'zle stare haslo'
#    return TemplateResponse(req, "changepass.html", {'msg':msg})

@login_required
def update_profile(req):
    form = ProfileForm(instance = req.user.profile, initial={
        'first_name':req.user.first_name,
        'last_name':req.user.last_name,
        'email':req.user.email,}
    )
    if req.method == 'POST':
        form = ProfileForm(req.POST, instance = req.user.profile)
        form.requser = req.user
        if form.is_valid():
            form.save()
            return HttpResponse('ok!')
        else:
            # XXX
            pass
    return TemplateResponse(req, "register.html", {"form": form})

from django.contrib.formtools.preview import FormPreview

class ProfileFormPreview(FormPreview):
    # preview_template = ...
    # form_template = ...

    def done(self, req, cleaned_data):
        form = ProfileForm(req.POST)
        form.save()
        # TODO send mail
        return TemplateResponse(req, "thanks.html")
