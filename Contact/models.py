from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from AuthenticationSystem.models import CustomUser


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    owner_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="contacts"
    )
    tags = models.ManyToManyField(
        Tag,
    )
    created_at = models.DateTimeField(auto_now_add=True)
