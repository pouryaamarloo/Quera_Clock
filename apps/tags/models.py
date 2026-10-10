from django.db import models
from core.models.base import TimestampedModel
from apps.workspaces.models import Workspace
from django.db.models import Q ,UniqueConstraint
from core.models.base import SoftDeleteQuerySet

class TagQuerySet(SoftDeleteQuerySet):
    def visible_to(self,user = None):
        if user is None or not user.is_authenticated:
            return self.none()
        return self.active().filter(workspace__workspace_membership__user=user,
                                    workspace__workspace_membership__is_active=True,
                                    workspace__workspace_membership__is_deleted=False)


class Tag(TimestampedModel):
    workspace =models.ForeignKey(Workspace,on_delete=models.CASCADE,related_name='tags')
    name =models.CharField(max_length=120)
    color =models.CharField(max_length=20 , default='#64748b')
    objects = TagQuerySet.as_manager()
    class Meta:
        ordering = ('name',)
        constraints = [UniqueConstraint(fields=['workspace','name'],condition =Q(is_deleted =False),name='unique_tag_name_per_workspace')]
# Create your models here.
    def __str__(self):
        return self.name