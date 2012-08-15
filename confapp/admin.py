from confapp.models import Conference, Profile, Payment
from django.contrib import admin

class ConferenceAdmin(admin.ModelAdmin):
	list_display = ('name', 'date')
	search_fields = ['name']

admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Profile)
admin.site.register(Payment)


