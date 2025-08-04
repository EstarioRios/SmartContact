from rest_framework import serializers
from .models import CustomUser, Ed_Class, Score


# ---------- SCORE ----------
class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ["id", "title", "value", "student"]


# ---------- READ-ONLY USER ----------
class CustomUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "user_type",
            "id_code",
            "active_mode",
        ]


# ---------- READ-ONLY USERTYPE ----------
class CustomUserUserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["user_type", "active_mode"]


# ---------- FULL USER DETAIL (nested) ----------
class CustomUserDetailSerializer(serializers.ModelSerializer):
    scores = ScoreSerializer(many=True, read_only=True)
    ed_class = serializers.StringRelatedField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "user_type",
            "id_code",
            "ed_class",
            "scores",
            "active_mode",
        ]


class CusomUserDetailSerializerTeacher(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "active_mode",
            "id_code",
            "user_type",
            "last_name",
            "first_name",
            "id",
            "classes",
        ]


# ---------- CREATE STUDENT ----------
class StudentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "id_code", "password", "ed_class"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_student(**validated_data)


# ---------- CREATE TEACHER ----------
class TeacherCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "id_code", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_teacher(**validated_data)


# ---------- CLASS ----------
class EdClassSerializer(serializers.ModelSerializer):
    students = CustomUserListSerializer(many=True, read_only=True)
    teacher = CustomUserListSerializer(read_only=True)

    class Meta:
        model = Ed_Class
        fields = ["id", "title", "teacher", "students"]
