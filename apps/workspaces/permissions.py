from .models import WorkspaceMembership

ROLE_RANK = {
    "owner" : 3 ,
    "admin" : 2 ,
    "manager" : 2 ,
    "member" : 1 ,
}


def get_workspace_membership(user, workspace):
    if user is None or not user.is_authenticated:
        return None
    return workspace.workspace_membership.filter(user=user, is_active=True, is_deleted=False).first()


def get_workspace_role(user, workspace):
    if user is None or not user.is_authenticated:
        return None
    if workspace.owner_id == user.id :
        return "owner"
    else :
        membership = WorkspaceMembership.objects.filter(user = user ,workspace = workspace , is_active = True ,is_deleted=False).first()
        if membership is None:
            return None
        return membership.role




def has_workspace_role(user, workspace, minimum_role):
    role = get_workspace_role(user, workspace)
    if role is None:
        return False
    if ROLE_RANK[role] >= ROLE_RANK[minimum_role]:
        return True
    return False
