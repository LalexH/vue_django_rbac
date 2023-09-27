from rest_framework.permissions import BasePermission


class Permission(BasePermission):
    def has_permission(self, request, view):
        url = "/{}/{}".format(request.path.split("/")[1], request.path.split("/")[2])
        method = request.method



        # user = jwt_decode_handler(request.META.get("HTTP_TOKEN", None))

        # 用户修改密码权限校验
        if url == "/api/user" and method == "PUT":
            uid = request.data["id"]
            s_uid = request.session["user"]["id"]
            if uid != s_uid:
                return False
            else:
                return True

        if url == "/api/userinfo":
            return True

        for per in request.session["permissions"]:
            if per["per_url"] == url and per["per_method"] == method:
                return True

        return False
