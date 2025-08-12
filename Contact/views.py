from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache

from .serializers import ContactSerializer, ContactListSerializer
from .models import Contact
from AuthenticationSystem.models import CustomUser


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_contact(request):
    contact_name = request.data.get("name")
    contact_phone_number = request.data.get("phone_number")
    contact_tags = request.data.get("tags")

    if not all([contact_name, contact_phone_number, contact_tags]):
        return Response(
            {
                "error": "all fields (contact_name, contact_phone_number, contact_tags) are required"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    user_auth = JWTAuthentication().authenticate(request)
    if not user_auth:
        return Response(
            {"error": "your JWT is not fine"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user, _ = user_auth
    contact_owner_user = user

    try:
        Contact.objects.create(
            name=contact_name,
            phone_number=contact_phone_number,
            owner_user=contact_owner_user,
            tags=contact_tags,
        )
        cache.delete(f"user_{user.id}_contacts")
        cache.delete_pattern(f"user_{user.id}_contacts_tag_*")
        return Response(
            {"msg": "was successfuly"},
            status=status.HTTP_201_CREATED,
        )
    except ValueError as e:
        return Response(
            {"error": f"{e}"},
            status=status.HTTP_403_FORBIDDEN,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def view_all_contacts(request):
    user_auth = JWTAuthentication().authenticate(request)
    if not user_auth:
        return Response(
            {"error": "your JWT is not fine"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    user, _ = user_auth

    cache_key = f"user_{user.id}_contacts"
    cached_data = cache.get(cache_key)
    if cached_data:
        return Response(
            {"msg": "was successful (from cache)", "contacts": cached_data},
            status=status.HTTP_200_OK,
        )

    try:
        user_contacts = user.contacts
    except ValueError as e:
        return Response(
            {"error": f"{e}"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serialized_data = ContactListSerializer(user_contacts).data
    cache.set(cache_key, serialized_data, timeout=60 * 5)
    return Response(
        {"msg": "was successful", "contacts": serialized_data},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def view_contacts_deppents_on_tag(request):
    user_auth = JWTAuthentication().authenticate(request)
    if not user_auth:
        return Response(
            {"error": "your JWT is not fine"}, status=status.HTTP_400_BAD_REQUEST
        )
    tag = request.query_params.get("tag", "").strip().lower()
    if not tag:
        return Response(
            {"error": "tag parameter is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    user, _ = user_auth

    cache_key = f"user_{user.id}_contacts_tag_{tag}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return Response(cached_data, status=status.HTTP_200_OK)

    user_contacts = user.contacts.all()
    final_contacts = []
    for contact in user_contacts:
        tags_of_contact = str(contact.tags)
        tags_list = [t.strip().lower() for t in tags_of_contact.split("-")]
        if tag in tags_list:
            final_contacts.append(contact)

    serializer = ContactSerializer(final_contacts, many=True)
    cache.set(cache_key, serializer.data, timeout=60 * 5)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_contact(request):
    user_auth = JWTAuthentication().authenticate(request)
    if not user_auth:
        return Response(
            {"error": "your JWT is not fine"}, status=status.HTTP_400_BAD_REQUEST
        )
    user, _ = user_auth
    contact_id = request.query_params.get("contact_id")

    if not contact_id:
        return Response(
            {"error": "(contact_id) is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        contact = Contact.objects.get(id=contact_id)
    except Contact.DoesNotExist:
        return Response(
            {"error": "Contact not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    contact_user = contact.owner_user

    if contact_user != user:
        return Response(
            {"error": "you are not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    contact.delete()
    cache.delete(f"user_{user.id}_contacts")
    cache.delete_pattern(f"user_{user.id}_contacts_tag_*")
    return Response({}, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_contact(request):
    user_auth = JWTAuthentication().authenticate(request)
    if not user_auth:
        return Response(
            {"error": "your JWT is not fine"}, status=status.HTTP_400_BAD_REQUEST
        )
    user, _ = user_auth

    new_phone_number = request.data.get("new_phone_number")
    contact_id = request.data.get("contact_id")
    new_name = request.data.get("new_name")
    new_tags = request.data.get("new_tags")

    if not all([new_phone_number, contact_id, new_name]):
        return Response(
            {"error": "(new_phone_number, contact_id, new_name) are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        contact = Contact.objects.get(id=contact_id)
    except Contact.DoesNotExist:
        return Response(
            {"error": "Contact not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if contact.owner_user != user:
        return Response(
            {"error": "you are not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    contact.phone_number = new_phone_number
    contact.name = new_name
    if new_tags:
        contact.tags = new_tags

    contact.save()
    cache.delete(f"user_{user.id}_contacts")
    cache.delete_pattern(f"user_{user.id}_contacts_tag_*")
    return Response({"msg": "Contact updated"}, status=status.HTTP_200_OK)
