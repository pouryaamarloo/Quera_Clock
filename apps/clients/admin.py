from django.contrib import admin
from .models import Client
from core.admins.base import SoftDeleteAdmin
@admin.register(Client)
class ClientAdmin(SoftDeleteAdmin):

    list_display = ('workspace' , 'name')
    search_fields = ('name',)
    list_filter = ('workspace',)
    ordering = ('-created_at',)
# Register your models here.
