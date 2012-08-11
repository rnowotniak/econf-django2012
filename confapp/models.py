from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Conference(models.Model):
	name = models.CharField(max_length = 255)
	date = models.DateField()
	email = models.EmailField()

	def __unicode__(self):
		return self.name

class Profile(models.Model):
	user = models.OneToOneField(User)
	organization = models.CharField(max_length = 255, blank = False)
	institute = models.CharField(max_length = 255)

	city = models.CharField(max_length = 50)
	postcode = models.CharField(max_length = 6)
	address = models.CharField(max_length = 255)

	nip = models.CharField(max_length = 30)
	phone = models.CharField(max_length = 255)

	def __unicode__(self):
		return '%s %s' % (self.user.first_name, self.user.last_name)

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

