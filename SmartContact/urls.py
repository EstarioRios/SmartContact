from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin panel
    path("admin/", admin.site.urls),
    # Authentication-related API endpoints (login, signup)
    path("api/auth/", include("AuthenticationSystem.urls")),
    # # Academy-related API endpoints (scores, classes, profiles)
    # path("api/", include("Academi.urls")),
]
