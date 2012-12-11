# -*- coding: utf-8 -*-

# Create your views here.
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import  send_mail
from django.core.mail.message import EmailMessage
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.views.generic.edit import   DeleteView, UpdateView
import mimetypes
import os
import smtplib
from confapp import forms
from confapp.forms import AccountForm
from confapp.models import Paper, Attachment, Review
from models import Account
from django.template.response import TemplateResponse

def main(req):
    if req.user.is_authenticated(): # logged in user
        if req.user.account.accounttype.id != 4: # not reviewer
            papers = Paper.objects.filter(account__id = req.user.account.id)
            accounts = []
            if req.user.is_staff:
                accounts = Account.objects.all()
            return TemplateResponse(req, "panel.html", {'papers':papers, 'accounts':accounts})
        else: # reviewer
            toreview = req.user.account.review_papers.all()
            return TemplateResponse(req, "panel.html", {'toreview':toreview})
    return HttpResponseRedirect('/login')
#    users = User.objects.all()
#    return TemplateResponse(req, "base.html", {"users": users})

@login_required
@transaction.commit_on_success
def update_account(req):
    form = AccountForm(instance = req.user.account, initial={
        'first_name':req.user.first_name,
        'last_name':req.user.last_name,
        'email':req.user.email,}
    )
    del form.fields['password']
    del form.fields['password2']
    if req.method == 'POST':
        form = AccountForm(req.POST, instance = req.user.account)
        del form.fields['password']
        del form.fields['password2']
        form.requser = req.user
        if form.is_valid():
            form.save()
            messages.success(req, 'Dane zaktualizowane')
            return HttpResponseRedirect('/')
    return TemplateResponse(req, "registration/register.html", {"form": form})

@login_required
def contact(req):
    if req.method == 'POST':
        form = forms.ContactForm(req.POST)
        if form.is_valid():
            try:
                if form.cleaned_data['sendcopy']:
                    send_mail(u'Kopia wiadomości do organizatorów Forum Innowacji Młodych Badaczy',
                        form.cleaned_data['message'], settings.SERVER_EMAIL, [req.user.email])
                managers = [m[1] for m in settings.MANAGERS]
                email = EmailMessage(u'[FIMB] Wiadomość od %s %s' % (unicode(req.user.account), req.user.email),
                    form.cleaned_data['message'], settings.SERVER_EMAIL, managers,
                    headers = {'Reply-To': req.user.email})
                email.send()
                messages.success(req, "Wiadomość została wysłana")
            except smtplib.SMTPException, e:
                print e
                return HttpResponse("Błąd podczas wysyłania wiadomości")
            return HttpResponseRedirect('/')
    else:
        form = forms.ContactForm()
    return TemplateResponse(req, "contact.html", {'form':form})

@login_required()
def get_attachment(req, id):
    try:
        attachment = Attachment.objects.get(id=id)
        if attachment.paper.account.user.id != req.user.id and attachment.paper.reviewer_id != req.user.id:
            # The logged user does not own the requested attachment, nor the logged user is the assigned reviewer
            raise Attachment.DoesNotExist
        file = attachment.file
        content = file.read()
    except Attachment.DoesNotExist:
        raise Http404('No such attachment')
    res = HttpResponse(content, mimetype = mimetypes.guess_type(str(file))[0])
    res['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(str(file))
    return res

@login_required
@transaction.commit_on_success
def review_paper(req, paper_id = None):
    if paper_id is None:
        return
    try:
        p = Paper.objects.get(id = paper_id)
        form = forms.ReviewForm(instance = p.review)
    except Paper.DoesNotExist:
        raise Http404('No such paper')
    except Review.DoesNotExist:
        form = forms.ReviewForm()
    if req.method == 'POST':
        try:
            form = forms.ReviewForm(req.POST, instance = p.review)
        except Review.DoesNotExist:
            form = forms.ReviewForm(req.POST)
        if form.is_valid():
            review = form.save(commit = False)
            review.paper = p
            review.save()
            messages.success(req, u'Dziękujemy za recenzję')
            return HttpResponseRedirect('/')
    return TemplateResponse(req, "papers/review.html", {'form': form, 'paper':p, 'attachment': p.attachment_set.order_by('-created')[0] })

@login_required
@transaction.commit_on_success
def paper(req, pk = None):
    if pk is not None:
        try:
            paper = Paper.objects.get(pk = pk)
            if paper.account.user_id != req.user.id:
                raise Paper.DoesNotExist
        except Paper.DoesNotExist, e:
            raise Http404('Nie ma takiego artykułu')
    attachments = None
    if req.method == 'POST':
        form = forms.PaperForm(req.POST, req.FILES)
        if pk is not None:
            form = forms.PaperForm(req.POST, req.FILES, instance = Paper.objects.get(pk = pk))
        if form.is_valid():
            paper = form.save(commit = False)
            paper.account = req.user.account
            paper.save()
            if req.FILES.has_key('attachment'):
                file = req.FILES['attachment']
                attachment = Attachment(type=form.cleaned_data['type'], file=file)
                attachment.paper = paper
                paper.attachment_set.add(attachment)
                attachment.save()
            messages.success(req, "Zgłoszenie referatu zostało %s." % ('przyjęte' if pk is None else 'zaktualizowane'))
            return HttpResponseRedirect('/')
    elif pk:
        paper = Paper.objects.get(pk = pk)
        form = forms.PaperForm(instance = paper)
        attachments = paper.attachment_set.all()
    else:
        form = forms.PaperForm(initial={'authors':req.user.account})
    return TemplateResponse(req, "papers/paper.html", {'form': form, 'attachments': attachments})

class PaperDelete(DeleteView):
    model = Paper
    success_url = '/'
    template_name = 'papers/delete.html'

    def get_context_data(self, **kwargs):
        context = super(PaperDelete, self).get_context_data(**kwargs)
        context['paper'] = self.object
        if self.get_object().account.user.id != self.request.user.id:
            raise Http404('Nie posiadasz takiego artykułu')
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PaperDelete, self).dispatch(*args, **kwargs)

    def delete(self, req, *args, **kwargs):
        result = super(PaperDelete, self).delete(req, *args, **kwargs)
        messages.success(req, 'Artykuł został usunięty.')
        return result

class ReviewUpdate(UpdateView):
    # TODO check if current user owns this article!
    model = Review
    template_name = 'review.html'
    success_url = '/'

#class PaperCreate(CreateView):
#    model = Paper
#    template_name = 'paper.html'
#    def get_initial(self):
#        # Get the initial dictionary from the superclass method
#        initial = super(PaperCreate, self).get_initial()
#        initial = initial.copy()
#        initial['authors'] = '%s %s' % (self.request.user.first_name, self.request.user.last_name)
#        return initial
#    def form_valid(self, form):
#        form.instance.account = self.request.user.account
#        return super(PaperCreate, self).form_valid(form)
#
#class PaperUpdate(UpdateView):
#    # TODO check if current user owns this article!
#    model = Paper
#    template_name = 'paper.html'
#    success_url = '/'

#def register(req):
#    form = AccountForm()
#    if req.method == 'POST':
#        form = AccountForm(req.POST)
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
