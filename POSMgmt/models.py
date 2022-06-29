from AccountMgmt.models import Account, regex_phone
from core.models import AuditMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


def tenancy_directory_path(instance, filename):
    # file will be uploaded to path config is below:
    return f"tenancy/POS_{instance.name}/%Y-%m-%d-{filename}"


class POS(AuditMixin):
    """Point Of Sale Model"""

    name = models.CharField(_("name"), max_length=255)
    address = models.CharField(_("address"), max_length=255)
    tenancy = models.FieldFile(_("tenancy agreement"), upload_to=tenancy_directory_path, null=True, blank=True)
    phone = models.CharField(_("store phone"), validators=[regex_phone], max_length=15, null=True, blank=True)
    price = models.IntegerField(_("rental amount"), validators=[MinValueValidator(0), MaxValueValidator(100000000)])
    active = models.BooleanField(_("active"), default=True)

    class Meta:
        verbose_name = _("POS")
        verbose_name_plural = _("POS Management")


class POSEmployees(AuditMixin):
    pos = models.ForeignKey(POS, on_delete=models.CASCADE, related_name="pos_employees")
    employee = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="employee_pos")
