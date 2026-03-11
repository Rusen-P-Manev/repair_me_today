from django.db import models


class Service(models.Model):
    name = models.CharField(
        max_length=300,
        verbose_name="Име на услугата",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за труд (лв.)",
    )

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return f"{self.name} - {self.price} лв."