from django.urls import path
from . import views

urlpatterns = [
    # Create a new contact (requires authentication)
    # Method: POST
    # Body: { "name": str, "phone_number": str, "tags": str }
    # Description: Creates a contact owned by the currently authenticated user
    path("create/", views.create_contact, name="create_contact"),

    # Retrieve all contacts of the authenticated user
    # Method: GET
    # Description: Returns a list of all contacts owned by the current user
    path("all/", views.view_all_contacts, name="view_all_contacts"),

    # Retrieve contacts filtered by a specific tag
    # Method: GET
    # Query param: ?tag=<tag_name>
    # Description: Returns only the contacts that contain the given tag
    # Tags in DB are stored as a single string separated by "-"
    path("by-tag/", views.view_contacts_deppents_on_tag, name="view_contacts_by_tag"),

    # Delete a specific contact by ID
    # Method: DELETE
    # Query param: ?contact_id=<id>
    # Description: Deletes the contact if it belongs to the current user
    path("delete/", views.delete_contact, name="delete_contact"),

    # Edit a specific contact
    # Method: PUT
    # Body: { "contact_id": int, "new_phone_number": str, "new_name": str, "new_tags": str (optional) }
    # Description: Updates contact details if it belongs to the current user
    path("edit/", views.edit_contact, name="edit_contact"),
]
