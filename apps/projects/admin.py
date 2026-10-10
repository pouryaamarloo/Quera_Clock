from django.contrib import admin
from .models import Project
from core.admins.base import SoftDeleteAdmin

@admin.register(Project)
class ProjectAdmin(SoftDeleteAdmin):

    list_display = ["workspace", "name" , "client","is_archived"]
    search_fields = ["name"]
    list_filter = ["workspace"]
    ordering = ["-created_at"]


# Register your models here.
