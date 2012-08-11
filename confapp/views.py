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

def main(req):
	users = Profile.objects.all()
	return render_to_response('main.html', {'users': users})

class ProfileForm(ModelForm):
	first_name = forms.CharField(max_length = 30)
	last_name = forms.CharField(max_length = 30)
	email = forms.EmailField()
	class Meta:
		model = Profile
		exclude = ('user',)

from django.views.decorators.cache import never_cache

@never_cache
@transaction.commit_on_success
def register(req):
	#return HttpResponse('register')
	formp = ProfileForm()
	if req.method == 'POST':
		#return HttpResponse(str(req.POST['email']))
		formp = ProfileForm(req.POST)
		if formp.is_valid():
			user = User.objects.create(
				first_name = formp.cleaned_data['first_name'],
				last_name  = formp.cleaned_data['last_name'],
				username   = formp.cleaned_data['email'],
				email      = formp.cleaned_data['email'])
			user.set_password('abc1')
			user.save()
			profile = formp.save(commit = False)
			profile.id = user.get_profile().id
			profile.user = user
			profile.save()
			# wyslanie maila potwierdzajacego rejestracje, login i haslo
			return HttpResponse('ok')
	return render_to_response('register.html', \
			{'formp':formp}, RequestContext(req))

