"""
URL configuration for codeguard_core project.
Configured with path-agnostic resolution protocols for Docker and Local execution bounds.
"""

from django.contrib import admin
from django.urls import path
from auditor.api import api as auditor_api  # Removed the hardcoded 'codeguard_backend' prefix

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", auditor_api.urls),
]