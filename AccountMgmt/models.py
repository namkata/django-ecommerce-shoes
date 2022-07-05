import enum

from core.models import AuditMixin
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

regex_phone = RegexValidator(r"^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$", "Invalid phone number")


@enum.unique
class AccountType(enum.Enum):
    Anonymous = "Anonymous"
    Consumer = "Consumer"
    Employee = "Employee"


class Account(AbstractUser):
    password = models.CharField(_("password"), max_length=128, null=True, blank=True)
    phone = models.CharField(_("phone"), max_length=15, validators=[regex_phone], null=True, blank=True)
    account_type = models.CharField(
        _("account type"),
        max_length=100,
        choices=((tag.value, tag.name) for tag in AccountType),
        default=AccountType.Employee.value,
    )

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")


class Account2FA(AuditMixin):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="account_2fa")
    is_phone = models.BooleanField(_("Phone number activated"), default=False)
    is_email = models.BooleanField(_("Email activated"), default=False)
    is_2fa = models.BooleanField(_("2FA activated"), default=False)
    pin = models.CharField(_("Security Code"), null=True, blank=True, max_length=100)
    is_security = models.BooleanField(_("Securiy code activated"), default=False)

    class Meta:
        verbose_name = _("Account 2FA")
        verbose_name_plural = _("Account 2FA Management")


@enum.unique
class EmployeePosition(enum.Enum):
    SalesAgent = "Sales Agent"
    HeadShops = "Head Shops"
    MgmtArea = "Management Area"
    Delivery = "Delivery"
    WHMgmt = "Warehouse Manager"
    Counselor = "Counselor"
    TechnicalStaff = "Technical Staff"
    HumanResourceMgmt = "Human Resource Management"
    Administration = "Administration"


@enum.unique
class AreaMgm(enum.Enum):
    Northern = "Northern"  # bac
    NCentral = "Northern Central"
    SCentral = "South Central"
    South = "South"


class EmployeePermission(AuditMixin):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="account_employee")
    position = models.CharField(
        _("position"),
        max_length=100,
        default=EmployeePosition.SalesAgent.value,
        choices=((tag.value, tag.name) for tag in EmployeePosition),
    )

    area = models.CharField(
        _("area"),
        max_length=100,
        null=True,
        blank=True,
        choices=((tag.value, tag.name) for tag in AreaMgm),
    )

    class Meta:
        verbose_name = _("Employee Permission")
        verbose_name_plural = _("Employee Permission Management")

    def __str__(self):
        return f"{self.account.get_full_name}-permission"


def contract_directory_path(instance, filename):
    # file will be uploaded to path config is below:
    return f"contract/account_{instance.account.email}/%Y-%m-%d-{filename}"


class EmploymentContract(AuditMixin):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="employment_contract")
    contract = models.FileField(_("contact files"), upload_to=contract_directory_path, null=True)
    price = models.IntegerField(_("wage"), default=0, validators=[MinValueValidator(0), MaxValueValidator(100000000)])
    is_quit = models.BooleanField(_("Is Quieted"), default=False)

    class Meta:
        verbose_name = _("Employment Contract")
        verbose_name_plural = _("Employment Contract Management")

    def __str__(self):
        return f"{self.account.get_full_name}-permission"


class StoreLogin(AuditMixin):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account_store")
    invocation_id = models.CharField(_("invocation id"), max_length=255)
    gmd_session = models.CharField(_("GDMSESSION"), max_length=255)
    active = models.BooleanField(_("active"), default=True)

    class Meta:
        verbose_name = _("Device Account")
        verbose_name_plural = _("Device Accounts")

    def __str__(self):
        return f"{self.account.get_full_name}-logged-in-ip-{self.invocation_id}-{self.gmd_session}"
