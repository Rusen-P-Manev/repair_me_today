from django.db import models


class RepairStatusChoices(models.TextChoices):
    RECEIVED = "received", "Приет"
    IN_PROGRESS = "in_progress", "В процес на работа"
    WAITING_PARTS = "waiting_parts", "Чака части"
    COMPLETED = "completed", "Завършен"


class PartStatusChoices(models.TextChoices):
    CLIENT_PROVIDED = "client_provided", "Осигурена от клиента"
    TO_ORDER = "to_order", "За поръчка"
    ORDERED = "ordered", "Поръчана"
    DELIVERED = "delivered", "Доставена"
    NOT_AVAILABLE = "not_available", "Не е налична"


class RepairJob(models.Model):
    vehicle = models.ForeignKey(
        "garage.Vehicle",
        on_delete=models.CASCADE,
        related_name="repairs",
        verbose_name="Автомобил",
    )

    problem_description = models.TextField(
        verbose_name="Описание на проблема от клиента",
    )

    received_by = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        null=True,
        related_name="received_jobs",
        verbose_name="Приел автомобила",
    )

    ordered_by = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ordered_parts_jobs",
        verbose_name="Поръчал части",
    )

    repaired_by = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="completed_jobs",
        verbose_name="Извършил ремонта",
    )

    services = models.ManyToManyField(
        "prices.Service",
        blank=True,
        related_name="repair_jobs",
        verbose_name="Извършени услуги (Труд)",
    )

    status = models.CharField(
        max_length=20,
        choices=RepairStatusChoices.choices,
        default=RepairStatusChoices.RECEIVED,
        verbose_name="Статус на ремонта",
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
        return f"Картон #{self.id} - {self.vehicle.vehicle_registration_number} ({self.get_status_display()})"


class RepairPart(models.Model):
    repair_job = models.ForeignKey(
        "RepairJob",
        on_delete=models.CASCADE,
        related_name="parts",
        verbose_name="Работен картон",
    )

    description = models.CharField(
        max_length=255,
        verbose_name="Описание на частта",
    )

    status = models.CharField(
        max_length=30,
        choices=PartStatusChoices.choices,
        default=PartStatusChoices.TO_ORDER,
        verbose_name="Статус на частта",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Цена (лв.)",
    )

    document_number = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Номер на документ",
    )

    class Meta:
        verbose_name = "Резервна част (към ремонт)"
        verbose_name_plural = "Резервни части (към ремонти)"

    def __str__(self):
        return f"{self.description} ({self.get_status_display()})"