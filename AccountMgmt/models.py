import enum
from datetime import datetime

from core.models import AuditMixin
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

EXPIRE_DATE = datetime.now() + settings.REFRESH_LIFE_TIME
regex_phone = RegexValidator(
    r"/^\s*(?:\+?(\d{1,3}))?([-. (]*(\d{3})[-. )]*)?((\d{3})[-. ]*(\d{2,4})(?:[-.x ]*(\d+))?)\s*$/gm",
    "Invalid phone number",
)


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
    remote_addr = models.CharField(_("remote address"), max_length=255)
    gmd_session = models.CharField(_("GDMSESSION"), max_length=255)
    active = models.BooleanField(_("active"), default=True)

    class Meta:
        verbose_name = _("Device Account")
        verbose_name_plural = _("Device Accounts")

    def __str__(self):
        return f"{self.account.get_full_name}-logged-in-ip-{self.invocation_id}-{self.gmd_session}"


class HistoryPassword(AuditMixin):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account_passwords")
    password_hash = models.CharField(_("descryption hash"), max_length=255)

    class Meta:
        verbose_name = _("History Password")
        verbose_name_plural = _("History Password Managements")

    def __str__(self):
        return f"{self.account.first_name}-{self.account.last_name}"


class HistoryRefreshToken(AuditMixin):
    store = models.OneToOneField(StoreLogin, on_delete=models.CASCADE, related_name="store_refresh_token")
    refresh_token = models.TextField(_("refresh token"))
    expire_date = models.DateTimeField(_("expire date"), default=EXPIRE_DATE)

    class Meta:
        verbose_name = _("History Refresh Token")
        verbose_name_plural = _("History Refresh Token Managements")

    def __str__(self):
        return f"{self.store.account.first_name}-{self.store.account.last_name}: refresh token"

    @property
    def is_expired(self):
        return datetime.now().timestamp() > self.expire_date.timestamp()


class HistoryAccessToken(AuditMixin):
    refresh = models.ForeignKey(HistoryRefreshToken, on_delete=models.CASCADE, related_name="store_access")
    access_token = models.TextField(_("access token"))

    class Meta:
        verbose_name = _("History Access Token")
        verbose_name_plural = _("History Access Token Managements")

    def __str__(self):
        return f"{self.refresh.store.account.first_name}-{self.refresh.store.account.last_name}: refresh token"

    @property
    def is_expired(self):
        return datetime.now().timestamp() > self.expire_date.timestamp()


class HistorySiginFailedOnDevices(AuditMixin):
    device = models.ForeignKey(
        StoreLogin, on_delete=models.CASCADE, related_name="device_failed", verbose_name=_("Device Connected")
    )
    num_failed = models.IntegerField(
        verbose_name=_("Number of Failured"), default=0, validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    active = models.BooleanField(verbose_name=_("Is active"), default=True)
    is_lock = models.BooleanField(verbose_name=_("Is Locked"), default=False)

    class Meta:
        verbose_name = _("History Account Sign In Failed")
        verbose_name_plural = _("List History Account Sign In Failed")

    def save(self, *args, **kwargs):
        if self.num_failed == 5:
            self.active = False
        super().save(*args, **kwargs)
