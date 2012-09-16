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

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/papers/%d' % self.id

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

