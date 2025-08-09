from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin
    # URL: /admin/
    path("admin/", admin.site.urls),

    # Authentication endpoints (mounted under /api/auth/)
    # Available endpoints (see AuthenticationSystem/urls.py):
    #   POST /api/auth/signup/         -> create new user (returns 201 with "msg","user","tokens")
    #   POST /api/auth/manual-login/   -> manual login with user_name+password (remember in body)
    #   POST /api/auth/login/          -> authenticate by JWT (Authorization: Bearer <access>)
    path("api/auth/", include("AuthenticationSystem.urls")),

    # Contact endpoints (mounted under /api/contact/)
    # Available endpoints (see Contact/urls.py):
    #   POST   /api/contact/create/    -> create contact (auth required)
    #   GET    /api/contact/all/       -> list all current user's contacts (auth required)
    #   GET    /api/contact/by-tag/?tag=<tag>
    #   DELETE /api/contact/delete/?contact_id=<id>
    #   PUT    /api/contact/edit/      -> edit contact (auth required)
    path("api/contact/", include("Contact.urls")),
]
