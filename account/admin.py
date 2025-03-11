from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    search_fields = ['frist_name', 'last_name']
    list_display = ['frist_name', 'last_name', 'user']
    autocomplete_fields = ['user']