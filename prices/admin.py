from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
    )
    list_filter = (
        "price",
    )
    search_fields = (
        "name",
    )