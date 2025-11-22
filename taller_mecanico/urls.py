"""Rutas principales del proyecto."""


from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from . import views
from django.conf import settings
from django.conf.urls.static import static


from django.contrib.auth import views as auth_views
from clientes.forms_auth import Loginforms

urlpatterns = [
    #urls para login y logout
    path("", lambda request: redirect("login/")),
    path("login/", auth_views.LoginView.as_view(template_name="login.html", authentication_form=Loginforms), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("admin/", admin.site.urls),
    path("home/", views.home, name="home"),
    path("clientes/", include("clientes.urls")),
    path("vehiculos/", include("vehiculo.urls")),
    path("cotizaciones/", include("cotizaciones.urls")),
    path('servicios/', include('servicios.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
