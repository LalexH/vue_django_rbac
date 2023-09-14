from django.forms import model_to_dict
from rest_framework import serializers

from data.models import SysUser, SysMenu, SysPermission, SysRole, SysRolePermission, SysRoleMenu, SysUserRole


class SysUserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()

    def get_role(self, obj):
        r_list = []
        for i in SysUserRole.objects.filter(user_id=obj.id):
            role_id = i.role_id
            role_obj = SysRole.objects.filter(id=role_id).first()

            r_list.append({"role_id": role_obj.id, "role_name": role_obj.role_name})
        return r_list

    def get_last_login(self, obj):
        return obj.last_login.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        model = SysUser
        fields = ["id", "is_superuser", "username", "email", "last_login", "role", "is_active", "phone"]


class SysMenuSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    route_path = serializers.CharField(allow_blank=True)

    def get_children(self, obj):
        c_list = []
        for i in SysMenu.objects.filter(parent_id=obj.id):
            c_list.append(model_to_dict(i))
        return c_list

    class Meta:
        model = SysMenu
        fields = ["id", "menu_title", "menu_icon", "route_path", "parent_id", "children"]


class SysPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysPermission
        fields = ["id", "per_name", "per_method", "per_url"]


class SysRoleSerializer(serializers.ModelSerializer):
    permission_list = serializers.SerializerMethodField()
    menu_list = serializers.SerializerMethodField()

    def get_permission_list(self, obj):
        per_id_list = list(SysRolePermission.objects.filter(role_id=obj.id).values_list("per_id", flat=True))
        c_list = []
        for i in SysPermission.objects.filter(id__in=per_id_list):
            c_list.append(model_to_dict(i))
        return c_list

    def get_menu_list(self, obj):
        menu_id_list = list(SysRoleMenu.objects.filter(role_id=obj.id).values_list("menu_id", flat=True))
        c_list = []
        for i in SysMenu.objects.filter(id__in=menu_id_list):
            c_list.append(model_to_dict(i))
        return c_list

    class Meta:
        model = SysRole
        fields = ["id", "role_name", "permission_list", "menu_list"]
