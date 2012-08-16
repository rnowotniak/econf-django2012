from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.formtools.preview import FormPreview
from confapp.forms import ProfileFormPreview, ProfileForm

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'econf.views.home', name='home'),
    # url(r'^econf/', include('econf.foo.urls')),

    (r'^$', 'confapp.views.main'),
    #(r'^register$', 'confapp.views.register'),

    (r'^register$', ProfileFormPreview(ProfileForm)),

    (r'^changepass$', 'django.contrib.auth.views.password_change'),
    (r'^changepassdone$', 'django.contrib.auth.views.password_change_done'),

    (r'^login$', 'django.contrib.auth.views.login'),
    (r'^logout$', 'django.contrib.auth.views.logout', {'next_page':'/'}),
#    (r'^login$', 'confapp.views.login'),
#    (r'^logout$', 'confapp.views.logout'),

    #(r'^changepass$', 'confapp.views.changepass'),
    (r'^profile/update$', 'confapp.views.update_profile'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
