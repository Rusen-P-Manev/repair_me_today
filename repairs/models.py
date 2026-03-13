import uuid
from django.db import models
from django.core.validators import MinValueValidator


class PartOrderStatusChoices(models.TextChoices):
    CLIENT_PROVIDED = "client_provided", "Части на клиента"
    WAITING_DELIVERY = "waiting_delivery", "Чака доставка"
    SEARCHING = "searching", "Търсят се"
    DELIVERED = "delivered", "Доставени"


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
        validators=[MinValueValidator(0.01)],
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
        validators=[MinValueValidator(0.01)],
        verbose_name="Количество / Часове",
    )

    class Meta:
        verbose_name = "Услуга към ремонт"
        verbose_name_plural = "Услуги към ремонти"

    def __str__(self):
        return f"{self.service.name} x {self.quantity}"

    class PartOrder(models.Model):
        repair_job = models.ForeignKey(
            "RepairJob",
            on_delete=models.CASCADE,
            related_name="parts",
            verbose_name="Работен картон",
        )

        status = models.CharField(
            max_length=20,
            choices=PartOrderStatusChoices.choices,
            default=PartOrderStatusChoices.WAITING_DELIVERY,
            verbose_name="Статус на частта",
        )

        description = models.CharField(
            max_length=255,
            verbose_name="Описание на частта/частите",
            help_text="Напр. Накладки, Маслен филтър и др."
        )

        invoice_number = models.CharField(
            max_length=50,
            blank=True,
            null=True,
            verbose_name="Номер на доставна фактура",
        )

        price = models.DecimalField(
            max_digits=10,
            decimal_places=2,
            blank=True,
            null=True,
            validators=[MinValueValidator(0.01)],
            verbose_name="Цена на частта",
        )

        class Meta:
            verbose_name = "Авточаст към ремонт"
            verbose_name_plural = "Авточасти към ремонти"

        def __str__(self):
            return f"{self.description} - {self.get_status_display()}"