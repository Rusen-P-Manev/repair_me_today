from django.db import models


class Employee(models.Model):
    first_name = models.CharField(
        max_length=20,
        verbose_name="Име",
    )

    last_name = models.CharField(
        max_length=20,
        verbose_name="Фамилия",
    )

    position = models.CharField(
        max_length=30,
        verbose_name="Длъжност",
    )

    class Meta:
        verbose_name = "Служител"
        verbose_name_plural = "Служители"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"