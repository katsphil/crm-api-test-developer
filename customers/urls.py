from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.authentication import TokenAuthentication

from .views import CustomerViewSet, UserViewSet, GoogleLogin, UserRedirectView

schema_view = get_schema_view(
    openapi.Info(
        title="CRM API",
        default_version="v1",
    ),
    public=True,
    authentication_classes=(TokenAuthentication,),
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r"customers", CustomerViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("rest-auth/", include("dj_rest_auth.urls")),
    path("rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path("rest-auth/google/", GoogleLogin.as_view(), name="google_login"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),
]
