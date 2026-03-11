from django.db import models


class Invoice(models.Model):
    repair_job = models.OneToOneField(
        "repairs.RepairJob",
        on_delete=models.CASCADE,
        related_name="invoice",
        verbose_name="Работен картон",
    )

    total_labor_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Общо за труд",
    )

    total_parts_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Общо за части",
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Крайна сума",
    )

    is_paid = models.BooleanField(
        default=False,
        verbose_name="Платена",
    )

    email_sent = models.BooleanField(
        default=False,
        verbose_name="Имейлът е изпратен",
    )

    archive_snapshot = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Архив (JSON Снимка на ремонта)",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Създадена на",
    )

    class Meta:
        verbose_name = "Фактура / Архив"
        verbose_name_plural = "Фактури / Архиви"

    def __str__(self):
        return f"Фактура за Картон #{self.repair_job.id} - Тотал: {self.total_amount} лв."