from confapp.models import Conference, Profile
from django.contrib import admin

class ConferenceAdmin(admin.ModelAdmin):
	list_display = ('name', 'date')
	search_fields = ['name']

admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Profile)


