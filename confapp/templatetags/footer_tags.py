import django
from django import template

register = template.Library()

@register.simple_tag
def footer():
	return "Django, wersja: %s" % django.get_version()


