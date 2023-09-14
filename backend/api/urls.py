from django.conf.urls import include
from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from api.views import PermissionViewSet, UserViewSet, RoleViewSet, MenuViewSet, UserInfoView, LoginView

router = DefaultRouter(trailing_slash=False)

# RBAC
router.register(r"user", UserViewSet)
router.register(r"role", RoleViewSet)
router.register(r"menu", MenuViewSet)
router.register(r"permission", PermissionViewSet)

urlpatterns = [
    path(r'login', LoginView.as_view()),
    path(r'userinfo', UserInfoView.as_view()),
    path('', include(router.urls)),
    path('docs', include_docs_urls(title='api')),
]
