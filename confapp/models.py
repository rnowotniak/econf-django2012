# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Conference(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    email = models.EmailField()

    def __unicode__(self):
        return self.name


class Review(models.Model):
    paper = models.OneToOneField('Paper')

    NO = 0
    PARTIALLY = 1
    YES = 2

    UNACCEPTABLE = 0
    ACCEPTABLE = 1
    GOOD = 2

    REJECT = 0
    REVIEW_REVISED = 1
    PUBLISH_REVISED = 2
    PUBLISH = 3

    CHOICES1 = (
        (NO, 'Nie'),
        (PARTIALLY, u'Częściowo'),
        (YES, 'Tak'),
    )
    CHOICES2 = (
        (UNACCEPTABLE, u'Niezadowalająca'),
        (ACCEPTABLE, u'Zadowalająca'),
        (GOOD, 'Bardzo dobra'),
    )
    CHOICES3 = tuple([(i+1, i+1) for i in range(5)])
    CHOICES4 = (
        (REJECT, u'Odrzucić'),
        (REVIEW_REVISED, u'Poprawioną wersję poddać ponownej recenzji'),
        (PUBLISH_REVISED, u'Opublikować po korekcie'),
        (PUBLISH, u'Opublikować bez poprawek'),
    )

    original = models.IntegerField(choices = CHOICES1, default = 0)
    significant = models.IntegerField(choices = CHOICES1, default = 0)
    clear = models.IntegerField(choices = CHOICES1, default = 0)
    correct = models.IntegerField(choices = CHOICES1, default = 0)
    citing = models.IntegerField(choices = CHOICES1, default = 0)
    figures = models.IntegerField(choices = CHOICES1, default = 0)

    adequacy = models.IntegerField(choices = CHOICES2, default = 0)
    novelty = models.IntegerField(choices = CHOICES2, default = 0)

    rating = models.IntegerField(choices = CHOICES3, default = 0)
    summary = models.IntegerField(choices = CHOICES4, default = 0)

    remarks = models.TextField(verbose_name='Remarks', blank=True)
    comments = models.TextField(verbose_name='Comments', blank=True)


class Account(models.Model):
    user = models.OneToOneField(User)

    organization = models.CharField(verbose_name='Organizacja', max_length=255)
    institute = models.CharField(verbose_name='Jednostka', max_length=255)
    city = models.CharField(verbose_name='Miasto', max_length=50)
    postcode = models.CharField(verbose_name='Kod pocztowy', max_length=6)
    address = models.CharField(verbose_name='Adres', max_length=255)

    nip = models.CharField(verbose_name='Numer NIP', max_length=30)

    accounttype = models.ForeignKey('AccountType', default=0, verbose_name='Uczestnictwo')

    phone = models.CharField(verbose_name='Telefon', max_length=255)

    address2 = models.TextField(verbose_name='Adres do korespondencji', blank=True)

    def __unicode__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


class AccountType(models.Model):
    name = models.CharField(max_length=30)
    payment = models.DecimalField(max_digits=6, decimal_places=2)

    def __unicode__(self):
        return '%s (%.2f PLN)' % (self.name, self.payment)


class Paper(models.Model):
    account = models.ForeignKey(Account, editable = False)
    title = models.CharField(max_length = 256, verbose_name=u'Tytuł')
    authors = models.CharField(max_length = 256, verbose_name='Autorzy')
    abstract = models.TextField(verbose_name="Abstrakt", blank = True)
    session = models.ForeignKey('SessionType', default = 0, verbose_name = 'Sesja')
    reviewer = models.ForeignKey(Account, editable = True, related_name= 'review_papers', null = True)

    def __unicode__(self):
        return '%s (Sesja %s)' % (self.title, str(self.session))

    def get_absolute_url(self):
        return '/papers/%d' % self.id


class SessionType(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class Attachment(models.Model):
    class Meta:
        ordering = ['-created']

    ARTICLE = 0
    PRESENTATION = 1
    TYPE_CHOICES = (
        (ARTICLE, 'Artykuł'),
        (PRESENTATION, 'Prezentacja'),
    )

    paper = models.ForeignKey(Paper, editable = False)
    created = models.DateTimeField(auto_now_add = True)
    type = models.IntegerField(choices = TYPE_CHOICES, default = ARTICLE)
    file = models.FileField(upload_to='attachments')

def create_user_account(sender, instance, created, **kwargs):
	if created:
		Account.objects.create(user=instance)

post_save.connect(create_user_account, sender=User)

