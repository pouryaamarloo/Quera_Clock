
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.core.exceptions import ValidationError
from django.utils import timezone

from core.models.base import TimestampedModel   # مسیر TimestampedModel خودت
from apps.workspaces.models import Workspace
from apps.projects.models import Project
from apps.tags.models import Tag
from core.models.base import SoftDeleteQuerySet


class TimeEntryQuerySet(SoftDeleteQuerySet):
    def visible_to(self,user=None):
        if user is None or not user.is_authenticated:
            return self.none()
        return self.active().filter(user=user)
    def running(self):
        return self.active().filter(end_time__isnull=True)

# ۱. اول QuerySet




# ۳. در نهایت مدل
class TimeEntry(TimestampedModel):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="time_entries",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="time_entries",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="time_entries",
    )
    tags = models.ManyToManyField(Tag, related_name="time_entries", blank=True)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    is_billable = models.BooleanField(default=False)

    # ۴. اتصال Manager
    objects =TimeEntryQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "time entries"
        ordering = ["-start_time", "-created_at"]
        constraints = [
            UniqueConstraint(
                fields=["workspace", "user"],
                condition=Q(end_time__isnull=True) & Q(is_deleted=False),
                name="unique_running_entry_per_user_workspace",
            ),
        ]

    @property
    def duration_seconds(self):
        if self.duration is None:
            return None
        return self.duration.total_seconds()

    def clean(self):
        super().clean()
        if self.project and self.project.workspace_id != self.workspace_id:
            raise ValidationError("Project must belong to the same workspace.")
        if self.end_time and self.start_time and self.end_time < self.start_time:
            raise ValidationError("End time must be after start time.")

    def save(self, *args, **kwargs):
        if self.end_time and self.start_time:
            duration = self.end_time - self.start_time
            self.duration = max(duration, timedelta(0))
        else:
            self.duration = None

        update_fields = kwargs.get("update_fields")
        if update_fields is not None:
            kwargs["update_fields"] = set(update_fields) | {"duration"}

        super().save(*args, **kwargs)

    def stop(self, ended_at=None):
        self.end_time = ended_at or timezone.now()
        self.full_clean()
        self.save()
        return self

    def __str__(self):
        return f"{self.user} {self.start_time}"


# Create your models here.
