# -*- coding: utf-8 -*-

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from confapp.forms import ProfileForm
from models import Profile
from django.template.response import TemplateResponse

def main(req):
    if req.user.is_authenticated():
        return TemplateResponse(req, "panel.html")
    users = Profile.objects.all()
    return TemplateResponse(req, "base.html", {"users": users})

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
