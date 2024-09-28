from django.contrib import admin
from main.models import Contact, IPAddressInfo, Project
# Register your models here.


@admin.register(IPAddressInfo)
class IPAddressInfoAdmin(admin.ModelAdmin):
    list_display = ('ip', 'city', 'country_name', 'created_at')
    search_fields = ('ip', 'city', 'country_name')
    list_filter = ('country_name', 'city')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

@admin.register(Project)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'btn1_text' , 'btn2_text', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)