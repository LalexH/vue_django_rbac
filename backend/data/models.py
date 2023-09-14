from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class SysUser(AbstractUser):
    username = models.CharField(verbose_name="用户名", max_length=128, unique=True)
    password = models.TextField()
    email = models.CharField(verbose_name="email", max_length=64, )
    phone = models.CharField(verbose_name="电话", max_length=64, )
    is_active = models.IntegerField(default=1)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        db_table = "sys_user"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
        unique_together = (("username",),)


class SysRole(models.Model):
    role_name = models.CharField(verbose_name="角色名称", max_length=64, unique=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        db_table = "sys_role"
        verbose_name = "角色表"
        verbose_name_plural = verbose_name
        unique_together = (("role_name",),)


class SysMenu(models.Model):
    menu_title = models.CharField(verbose_name="菜单title", max_length=64, )
    menu_icon = models.CharField(verbose_name="菜单图标", max_length=64, )
    route_path = models.CharField(verbose_name="route_path", max_length=128, default="")
    parent_id = models.IntegerField(verbose_name="parent_id", default=0, )
    index = models.IntegerField(verbose_name="优先级", default=0, )
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        db_table = "sys_menu"
        verbose_name = "菜单表"
        verbose_name_plural = verbose_name
        unique_together = (("menu_title", "route_path"),)



class SysPermission(models.Model):
    per_name = models.CharField(verbose_name="权限名称", max_length=128)
    per_method = models.CharField(verbose_name="方法", max_length=64)
    per_url = models.CharField(verbose_name="url", max_length=128)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        db_table = "sys_permission"
        verbose_name = "权限表"
        verbose_name_plural = verbose_name
        unique_together = (("per_name", "per_method"),)


class SysUserRole(models.Model):
    user_id = models.IntegerField(verbose_name="用户ID")
    role_id = models.IntegerField(verbose_name="角色ID")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        db_table = "sys_user_role"
        verbose_name = "用户角色关系表"
        verbose_name_plural = verbose_name
        unique_together = (("user_id", "role_id"),)


class SysRoleMenu(models.Model):
    role_id = models.IntegerField(verbose_name="角色ID")
    menu_id = models.IntegerField(verbose_name="菜单ID")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        db_table = "sys_role_menu"
        verbose_name = "角色菜单关系表"
        verbose_name_plural = verbose_name
        unique_together = (("role_id", "menu_id"),)


class SysRolePermission(models.Model):
    role_id = models.IntegerField(verbose_name="角色ID")
    per_id = models.IntegerField(verbose_name="权限ID")

    class Meta:
        db_table = "sys_role_permission"
        verbose_name = "角色权限关系表"
        verbose_name_plural = verbose_name
        unique_together = (("role_id", "per_id"),)
