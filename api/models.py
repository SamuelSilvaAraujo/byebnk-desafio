import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CommonModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Atualizado em")
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        abstract = True
        ordering = ("-created_at",)


class Asset(CommonModel):

    class ModeChoices(models.TextChoices):
        fixed_income = "fixed-income", "Renda fixa"
        variable_income = "variable-income", "Renda Variável"
        crypto = "crypto", "Cripto Moeda"

    name = models.CharField(max_length=100)
    mode = models.CharField(max_length=100, choices=ModeChoices.choices)

    def __str__(self):
        return "{} - {}".format(self.name, self.get_mode_display())


class Transaction(CommonModel):
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    amount = models.IntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=12)
    ip_address = models.CharField(max_length=15)
    request_date = models.DateTimeField()
    is_redemption = models.BooleanField()

    def __str__(self):
        return "{} - {}".format(self.asset, self.ip_address)
