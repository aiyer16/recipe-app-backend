"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Recipe API",
        default_version='v1',
        description="API to interact with backend of Recipe App",
        contact=openapi.Contact(email="akshay.rajagopal@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    authentication_classes=(TokenAuthentication,),
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Swagger generator
    path('api/index', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),

    # Project URLs
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/recipe/', include('recipe.urls')),
]
