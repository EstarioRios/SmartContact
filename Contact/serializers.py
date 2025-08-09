from rest_framework import serializers
from .models import Contact


# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "name"
