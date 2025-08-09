from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin panel
    path("admin/", admin.site.urls),
    # Authentication-related API endpoints (login, signup)
    path("api/auth/", include("AuthenticationSystem.urls")),
    # Contact-related API endpoints (create_contact, view_all_contacts, view_contacts_deppents_on_tag, delete_contact, edit_contact)
    path("api/contact", include("Contact.urls")),
]
