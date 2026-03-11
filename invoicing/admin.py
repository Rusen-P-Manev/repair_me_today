from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "repair_job",
        "total_amount",
        "is_paid",
        "email_sent",
        "created_at",
    )
    list_filter = (
        "is_paid",
        "email_sent",
        "created_at",
    )
    search_fields = (
        "repair_job__vehicle__license_plate",
    )
    readonly_fields = (
        "created_at",
    )