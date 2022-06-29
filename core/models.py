from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class AuditMixin(models.Model):
    created = models.DateTimeField(verbose_name=_("Created At"), editable=False, default=timezone.now, db_index=True)
    updated = models.DateTimeField(verbose_name=_("Updated At"), editable=False, default=timezone.now, db_index=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        dt = timezone.now()
        if self.pk:
            self.updated = dt

        super().save(*args, **kwargs)
