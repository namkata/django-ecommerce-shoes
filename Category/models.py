from core.models import AuditMixin
from django.core.validators import MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


class Category(AuditMixin):
    name = models.CharField(_("name"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=255)
    child_id = models.IntegerField(_("Category"), validators=[MinValueValidator(0)])
    grandchild_id = models.IntegerField(_("Category"), validators=[MinValueValidator(0)])
    description = models.TextField(_("description"))
    active = models.BooleanField(_("active"), default=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self) -> str:
        return f"category: {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
