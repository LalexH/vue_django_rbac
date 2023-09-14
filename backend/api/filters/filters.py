import django_filters

from data.models import SysMenu, SysUser


class SysMenuFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = SysMenu
        fields = ["menu_title"]


class SysUserFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = SysUser
        fields = ["username"]
