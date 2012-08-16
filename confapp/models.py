from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Conference(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    email = models.EmailField()

    def __unicode__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User)

    organization = models.CharField(verbose_name='Organizacja', max_length=255)
    institute = models.CharField(verbose_name='Jednostka', max_length=255)
    city = models.CharField(verbose_name='Miasto', max_length=50)
    postcode = models.CharField(verbose_name='Kod pocztowy', max_length=6)
    address = models.CharField(verbose_name='Adres', max_length=255)

    nip = models.CharField(verbose_name='Numer NIP', max_length=30)

    payment = models.ForeignKey('Payment', default=0, verbose_name='Uczestnictwo')

    phone = models.CharField(verbose_name='Telefon', max_length=255)

    address2 = models.TextField(verbose_name='Adres do korespondencji', blank=True)

    def __unicode__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


class Payment(models.Model):
    name = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __unicode__(self):
        return '%s (%.2f)' % (self.name, self.amount)

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

