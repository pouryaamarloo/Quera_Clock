from django.db import models
from core.models import TimestampedModel
from apps.workspaces.models import Workspace
from apps.clients.models import Client
from django.db.models import Q,UniqueConstraint
from django.core.exceptions import ValidationError
from core.models.base import SoftDeleteQuerySet

class ProjectQuerySet(SoftDeleteQuerySet) :
    def visible_to(self,user = None):
        if user is None or not user.is_authenticated:
            return self.none()
        return self.active().filter(workspace__workspace_membership__user=user,
                                    workspace__workspace_membership__is_active=True,
                                    workspace__workspace_membership__is_deleted=False)

    def not_archived(self):
        return self.filter(is_archived=False)


class Project(TimestampedModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE,related_name="projects")
    client = models.ForeignKey(Client, on_delete=models.SET_NULL,null=True,blank=True)
    name =models.CharField(max_length=255)
    color =models.CharField(max_length=20 ,default="#2563eb")
    description =models.TextField(blank=True,null=True)
    thumbnail =models.ImageField(upload_to ="projects/",blank=True,null=True)
    is_archived = models.BooleanField(default=False)
    objects = ProjectQuerySet.as_manager()
    class Meta:
        ordering = ["name"]
        constraints = [UniqueConstraint(fields=["workspace","name"],condition =Q(is_deleted =False) ,name="unique_project_name_per_workspace")]

    def clean(self):
        super().clean()
        if self.workspace and self.client:
            if self.client.workspace_id != self.workspace.id:
                raise ValidationError({
                   'client': 'Client must belong to the same workspace.'
                })
    def __str__(self):
        return self.name

# Create your models here.
