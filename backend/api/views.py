from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken
from datetime import datetime
from data import models

from api.filters.filters import SysMenuFilter, SysUserFilter
from api.serializers.serializers import SysUserSerializer, SysRoleSerializer, SysMenuSerializer, \
    SysPermissionSerializer
from data.models import SysUser, SysPermission, SysMenu, SysRole, SysRolePermission, SysRoleMenu, SysUserRole


class UserViewSet(ModelViewSet):
    queryset = SysUser.objects.all()
    serializer_class = SysUserSerializer
    lookup_field = "id"
    filter_class = SysUserFilter

    def create(self, request, *args, **kwargs):
        SysUser.objects.create_user(
            request.data["username"], request.data["email"],
            request.data["password"], **{"phone": request.data["phone"]})

        user_id = SysUser.objects.filter(username=request.data["username"]).first().id

        for role_id in request.data["role_id_list"]:
            SysUserRole.objects.update_or_create(role_id=role_id, user_id=user_id)

        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        # 重置密码
        if "password" in request.data:
            user_obj = models.SysUser.objects.filter(id=request.data["id"]).first()
            user_obj.set_password(request.data["password"])
            user_obj.save()
            return Response()

        data = request.data.copy()
        user_id = request.data["id"]
        SysUser.objects.update_or_create(id=user_id, defaults=data)

        if "role_id_list" not in data:
            return Response()

        data.pop("role_id_list")

        for role_id in request.data["role_id_list"]:
            SysUserRole.objects.update_or_create(role_id=role_id, user_id=user_id)

        for i in SysUserRole.objects.filter(user_id=user_id):
            if i.role_id not in request.data["role_id_list"]:
                SysUserRole.objects.filter(user_id=user_id, role_id=i.role_id).delete()

        return Response()

    def destroy(self, request, *args, **kwargs):
        user_id = request.data["id"]
        SysUser.objects.filter(id=user_id).delete()
        SysUserRole.objects.filter(user_id=user_id).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RoleViewSet(ModelViewSet):
    queryset = SysRole.objects.all()
    serializer_class = SysRoleSerializer
    lookup_field = "id"

    def create(self, request, *args, **kwargs):
        SysRole.objects.update_or_create(role_name=request.data["role_name"])

        role_id = SysRole.objects.filter(role_name=request.data["role_name"]).first().id

        for per_id in request.data["pers"]:
            SysRolePermission.objects.create(role_id=role_id, per_id=per_id)

        for menu_id in request.data["menus"]:
            SysRoleMenu.objects.create(role_id=role_id, menu_id=menu_id)

        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        role_id = request.data["id"]

        qs = SysUserRole.objects.filter(role_id=role_id)
        if qs:
            return Response(status=status.HTTP_301_MOVED_PERMANENTLY)

        SysRole.objects.filter(id=role_id).delete()
        SysRoleMenu.objects.filter(role_id=role_id).delete()
        SysRolePermission.objects.filter(role_id=role_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        role_id = request.data["id"]

        for i in SysRolePermission.objects.filter(role_id=role_id):
            if i.per_id not in request.data["pers"]:
                i.delete()
        for i in SysRoleMenu.objects.filter(role_id=role_id):
            if i.menu_id not in request.data["menus"]:
                i.delete()

        for per_id in request.data["pers"]:
            SysRolePermission.objects.update_or_create(role_id=role_id, per_id=per_id)

        for menu_id in request.data["menus"]:
            SysRoleMenu.objects.update_or_create(role_id=role_id, menu_id=menu_id)

        return Response()


class MenuViewSet(ModelViewSet):
    queryset = SysMenu.objects.all().order_by('index')
    serializer_class = SysMenuSerializer
    lookup_field = "id"
    filter_class = SysMenuFilter

    def destroy(self, request, *args, **kwargs):
        menu_id = request.data["id"]

        qs = SysRoleMenu.objects.filter(menu_id=menu_id)
        if qs:
            return Response(status=status.HTTP_301_MOVED_PERMANENTLY)

        SysMenu.objects.filter(id=menu_id).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PermissionViewSet(ModelViewSet):
    queryset = SysPermission.objects.all()
    serializer_class = SysPermissionSerializer

    def create(self, request, *args, **kwargs):
        act_dict = {"GET": "查看", "POST": "添加", "PUT": "修改", "DELETE": "删除"}
        data = request.data.copy()
        for per_method in request.data["per_method"]:
            data["per_method"] = per_method
            data["per_name"] = "{}{}".format(request.data["per_name"], act_dict[per_method])
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        per_id = request.data["id"]

        qs = SysRolePermission.objects.filter(per_id=per_id)
        if qs:
            return Response(status=status.HTTP_301_MOVED_PERMANENTLY)

        SysPermission.objects.filter(id=per_id).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserInfoView(APIView):
    def get(self, request):
        token = {}
        token["token"] = request.META.get('HTTP_TOKEN', None)
        valid_data = VerifyJSONWebTokenSerializer().validate(token)
        user = valid_data['user']

        user_obj = models.SysUser.objects.filter(username=user.username).first()

        user_info = {
            "id": user_obj.id,
            "username": user_obj.username,
            "email": user_obj.email,
            "phone": user_obj.phone,
        }

        role_id_list = list(models.SysUserRole.objects.filter(user_id=user_obj.id).values_list("role_id", flat=True))

        roles = []
        for i in models.SysRole.objects.filter(id__in=role_id_list):
            roles.append({
                "id": i.id,
                "role_name": i.role_name
            })

        permissions = get_permission(role_id_list)

        menus = get_menu(role_id_list, True if user_obj.is_superuser == 1 else False)

        request.session['permissions'] = permissions
        request.session['user'] = user_info

        data = {
            "user": user_info,
            "roles": roles,
            "menus": menus,
            "permissions": permissions,
        }

        return Response(data)


def get_permission(role_id_list):
    permissions = []
    per_id_list = list(
        models.SysRolePermission.objects.filter(role_id__in=role_id_list).values_list("per_id", flat=True))

    for per_obj in models.SysPermission.objects.filter(id__in=per_id_list):
        permissions.append({
            "per_name": per_obj.per_name,
            "per_method": per_obj.per_method,
            "per_url": per_obj.per_url}
        )

    return permissions


def get_menu(role_id_list, is_super=False):
    menus = []

    if is_super:
        menus_id_list = list(models.SysMenu.objects.all().values_list("id", flat=True))
    else:
        menus_id_list = list(
            models.SysRoleMenu.objects.filter(role_id__in=role_id_list).values_list("menu_id", flat=True))

    for menus_obj in models.SysMenu.objects.filter(id__in=menus_id_list, parent_id=0).order_by('index'):
        menus_dict = {
            "id": menus_obj.id,
            "menu_title": menus_obj.menu_title,
            "menu_icon": menus_obj.menu_icon,
            "route_path": menus_obj.route_path,
            "parent_id": menus_obj.parent_id,
            "children": []
        }

        for child_menus_obj in models.SysMenu.objects.filter(
                id__in=menus_id_list, parent_id=menus_obj.id).order_by('index'):
            menus_dict["children"].append({
                "id": child_menus_obj.id,
                "menu_title": child_menus_obj.menu_title,
                "menu_icon": child_menus_obj.menu_icon,
                "route_path": child_menus_obj.route_path,
                "parent_id": child_menus_obj.parent_id,
            })

        menus.append(menus_dict)

    return menus


jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class LoginView(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)

            # username = request.data["username"]
            # password = request.data["password"]
            # u = authenticate(request, username=username, password=password)
            # if u is not None:
            #     login(request, u)

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
