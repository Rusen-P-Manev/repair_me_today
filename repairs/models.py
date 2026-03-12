import uuid
from django.db import models


class RepairStatusChoices(models.TextChoices):
    RECEIVED = "received", "Приет"
    IN_PROGRESS = "in_progress", "В процес на работа"
    WAITING_PARTS = "waiting_parts", "Чака части"
    COMPLETED = "completed", "Завършен"


class Service(models.Model):
    name = models.CharField(
        max_length=300,
        verbose_name="Име на услугата",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена труд (лв.)",
    )

    class Meta:
        verbose_name = "Услуга (Ценоразпис)"
        verbose_name_plural = "Услуги (Ценоразпис)"

    def __str__(self):
        return f"{self.name} - {self.price} лв."


class RepairJob(models.Model):
    vehicle = models.ForeignKey(
        "garage.Vehicle",
        on_delete=models.CASCADE,
        related_name="repairs",
        verbose_name="Автомобил",
    )

    problem_description = models.TextField(
        verbose_name="Описание на проблема",
    )

    received_by = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        null=True,
        related_name="received_jobs",
        verbose_name="Приел автомобила",
    )

    repaired_by = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="completed_jobs",
        verbose_name="Извършил ремонта",
    )

    # Many-to-Many през междинен модел за количество
    services = models.ManyToManyField(
        "Service",
        through="RepairService",
        blank=True,
        related_name="repair_jobs",
        verbose_name="Извършени услуги",
    )

    status = models.CharField(
        max_length=20,
        choices=RepairStatusChoices.choices,
        default=RepairStatusChoices.RECEIVED,
        verbose_name="Статус на ремонта",
    )

    access_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="Код за проследяване",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Създаден на",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Последна промяна",
    )

    class Meta:
        verbose_name = "Работен картон"
        verbose_name_plural = "Работни картони"

    def __str__(self):
        return f"Картон #{self.id} - {self.vehicle.vehicle_registration_number}"


class RepairService(models.Model):
    repair_job = models.ForeignKey(
        "RepairJob",
        on_delete=models.CASCADE,
        verbose_name="Работен картон",
    )

    service = models.ForeignKey(
        "Service",
        on_delete=models.CASCADE,
        verbose_name="Избрана услуга",
    )

    quantity = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.00,
        verbose_name="Количество / Часове",
    )

    class Meta:
        verbose_name = "Услуга към ремонт"
        verbose_name_plural = "Услуги към ремонти"

    def __str__(self):
        return f"{self.service.name} x {self.quantity}"