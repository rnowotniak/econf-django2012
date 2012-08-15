from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.formtools.preview import FormPreview
from confapp.views import ProfileFormPreview, ProfileForm

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'econf.views.home', name='home'),
    # url(r'^econf/', include('econf.foo.urls')),

    (r'^$', 'confapp.views.main'),
    (r'^register$', 'confapp.views.register'),

    (r'^prev/$', ProfileFormPreview(ProfileForm)),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
