import django
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='dir')
def mydir(value):
    return mark_safe('<pre>%s</pre>' % str(dir(value)).replace(',',',\n'))

#register.filter('dir', mydir)