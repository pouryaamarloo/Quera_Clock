from django.db import models
from core.models import TimestampedModel
from apps.users.models import User
from django.db.models import Q,UniqueConstraint
from core.models.base import SoftDeleteQuerySet,SoftDeleteManager


class WorkspaceQuerySet(SoftDeleteQuerySet) :

    def visible_to(self,user=None):
        if user is None or not user.is_authenticated:
            return self.none()

        return self.filter(workspace_membership__user=user, workspace_membership__is_active=True, workspace_membership__is_deleted=False)


class WorkspaceMembershipQuerySet(SoftDeleteQuerySet):
    def enabled(self):
        return self.active().filter(is_deleted=False,is_active=True)

    def for_user(self,user = None):
        if user is None :
            return self.none()
        return self.active().filter(workspace__owner=user,is_deleted=False)

class Workspace(TimestampedModel):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='workspaces/', blank=True, null=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='owned_workspaces')
    objects = SoftDeleteManager.from_queryset(WorkspaceQuerySet)()

    class Meta:
        ordering = ['name' , 'created_at']
        constraints = [UniqueConstraint(fields=['name','owner'],condition=Q(is_deleted = False) ,name='unique_workspace_name_per_owner')]

    def __str__(self):
        return self.name


class WorkspaceMembership(TimestampedModel):

    class Role(models.TextChoices):
        OWNER = 'owner','Owner'
        ADMIN = 'admin','Admin'
        MEMBER = 'member','Member'

    workspace = models.ForeignKey(Workspace,on_delete=models.CASCADE,related_name='workspace_membership')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='workspace_membership')
    role = models.CharField(choices=Role.choices,max_length=10,default=Role.MEMBER)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    objects = WorkspaceMembershipQuerySet.as_manager()

    class Meta:
        ordering = ['workspace__name', 'user__mobile']
        constraints = [UniqueConstraint(fields=['workspace' , 'user'],condition = Q(is_deleted = False) ,name='unique_workspace_membership')]
# Create your models here.
    def __str__(self):
        return f"{self.user} {self.workspace.name}"



