from main.models import *


class Permissions(BaseModel):
    id = BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=255, default="")
    group_id = models.IntegerField()
    slug = models.CharField(max_length=255, default="")
    parent = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'permissions'


class PermissionGroups(BaseModel):
    id = BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'permission_groups'


class RolePermission(BaseModel):
    id = BigAutoField(primary_key=True)
    role_id = models.IntegerField()
    permission_id = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        db_table = 'role-permission'


class UserRole(BaseModel):
    id = BigAutoField(primary_key=True)
    staff_id = models.IntegerField()
    role_id = models.IntegerField()

    class Meta:
        db_table = 'role-user'



class UserPermission(BaseModel):
    id = BigAutoField(primary_key=True)
    staff_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        db_table = 'permission-user'
