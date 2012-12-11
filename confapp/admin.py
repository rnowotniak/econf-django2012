from confapp.models import Conference, Account, AccountType, Paper, Attachment, Review
from django.contrib import admin

class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    search_fields = ['name']

admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Account)
admin.site.register(AccountType)
admin.site.register(Review)

class AttachmentInline(admin.StackedInline):
    model = Attachment

class PaperAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline,]

admin.site.register(Paper, PaperAdmin)

