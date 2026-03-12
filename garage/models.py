from django.db import models


class Client(models.Model):
    is_corporate = models.BooleanField(
        default=False,
        verbose_name="Юридическо лице",
    )

    company_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Име на юридическо лице",
    )

    eik = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        verbose_name="ЕИК/Булстат",
    )

    address_city = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Град",
    )

    address_street = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Улица и №",
    )

    address_zip = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Пощенски код",
    )

    first_name = models.CharField(
        max_length=20,
        verbose_name="Име / МОЛ",
    )

    last_name = models.CharField(
        max_length=20,
        verbose_name="Фамилия",
    )

    phone_number = models.CharField(
        max_length=20,
        verbose_name="Телефон",
    )

    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Имейл",
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенти"

    def __str__(self):
        if self.is_corporate and self.company_name:
            return f"{self.company_name} ({self.eik})"
        return f"{self.first_name} {self.last_name}"


class Vehicle(models.Model):
    client = models.ForeignKey(
        "Client",
        on_delete=models.CASCADE,
        related_name="vehicles",
        verbose_name="Собственик",
    )

    vehicle_registration_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Регистрационен номер",
    )

    make = models.CharField(
        max_length=15,
        verbose_name="Марка",
    )

    model = models.CharField(
        max_length=15,
        verbose_name="Модел",
    )

    year = models.PositiveIntegerField(
        verbose_name="Година на производство",
    )

    vin = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="VIN номер",
    )

    class Meta:
        verbose_name = "Автомобил"
        verbose_name_plural = "Автомобили"

    def __str__(self):
        return f"{self.vehicle_registration_number} - {self.make} {self.model}"