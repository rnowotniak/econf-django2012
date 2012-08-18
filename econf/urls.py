from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.formtools.preview import FormPreview
from confapp.forms import AccountFormPreview, AccountForm
from confapp.views import PaperDelete

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'econf.views.home', name='home'),
    # url(r'^econf/', include('econf.foo.urls')),

    (r'^$', 'confapp.views.main'),

    #(r'^register$', 'confapp.views.register'),
    (r'^register$', AccountFormPreview(AccountForm)),
    (r'^accounts/profile/$', 'confapp.views.update_account'),
    (r'^contact$', 'confapp.views.contact'),

    (r'^papers/delete/(?P<pk>\d+)$', PaperDelete.as_view()),
    (r'^papers/$', 'confapp.views.paper'),
    (r'^papers/(?P<pk>\d+)$', 'confapp.views.paper'),
#    (r'^papers/(?P<pk>\d+)$', PaperUpdate.as_view()),
#    (r'^papers/$', PaperCreate.as_view()),

    (r'^attachments/(?P<id>\d+)$', 'confapp.views.get_attachment'),

    (r'^accounts/changepass/$', 'django.contrib.auth.views.password_change'),
    (r'^accounts/changepassdone$', 'django.contrib.auth.views.password_change_done'),
    (r'^login$', 'django.contrib.auth.views.login'),
    (r'^logout$', 'django.contrib.auth.views.logout', {'next_page':'/'}),

#    (r'^login$', 'confapp.views.login'),
#    (r'^logout$', 'confapp.views.logout'),
    #(r'^changepass$', 'confapp.views.changepass'),


    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )