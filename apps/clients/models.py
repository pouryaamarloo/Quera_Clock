from django.db import models
from apps.workspaces.models import Workspace
from core.models.base import TimestampedModel
from django.db.models import Q
from core.models.base import SoftDeleteQuerySet

class ClientQuerySet(SoftDeleteQuerySet):
    def visible_to(self,user=None):
        if user is None or not user.is_authenticated :
            return self.none()
        return self.active().filter(workspace__workspace_membership__user=user,
                                    workspace__workspace_membership__is_active=True,
                                    workspace__workspace_membership__is_deleted=False)


class Client(TimestampedModel):
    workspace = models.ForeignKey(Workspace,on_delete=models.CASCADE ,related_name='clients')
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='clients',blank=True, null=True)

    objects = ClientQuerySet.as_manager()

    class Meta:
        ordering =(
            'name',)
        constraints = [
            models.UniqueConstraint(fields=['name','workspace'],condition=Q(is_deleted = False) ,name='unique_client_name_per_workspace')
        ]
# Create your models here.
    def __str__(self):
        return f"{self.name}"