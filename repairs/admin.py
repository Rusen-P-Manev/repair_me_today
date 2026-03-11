from django.contrib import admin
from .models import RepairJob, RepairPart


@admin.register(RepairJob)
class RepairJobAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "vehicle",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "created_at",
    )
    search_fields = (
        "vehicle__license_plate",
        "vehicle__vin",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(RepairPart)
class RepairPartAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "repair_job",
        "status",
        "price",
    )
    list_filter = (
        "status",
    )
    search_fields = (
        "description",
        "repair_job__vehicle__license_plate",
    )