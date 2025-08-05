from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import CustomUser
from .serializers import (
    CustomUserSerializer,
)


# Generate JWT access and refresh tokens for a user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user=user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


# Dashboard Response Generator
def choose_dashboard(user, tokens, msg="Login successful", remember=False):
    if not tokens:
        return Response(
            {
                "success": msg,
                "user": CustomUserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )
    else:
        if remember in [True, "true", "True", 1, "1"]:

            return Response(
                {
                    "success": msg,
                    "tokens": tokens,
                    "user": CustomUserSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "success": msg,
                    "user": CustomUserSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )


# Admin-only signup view
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):

    # Extract new user data
    user_password = request.data.get("password")
    user_name = request.data.get("user_name")
    user_first_name = request.data.get("first_name")
    user_last_name = request.data.get("last_name")

    # Check for required fields
    if not all(
        [
            user_password,
            user_name,
        ]
    ):
        return Response(
            {"error": "All fields ( user_password, user_name) are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        try:
            user = CustomUser.objects.create_user(
                first_name=user_first_name,
                last_name=user_last_name,
                user_name=user_name,
                password=user_password,
            )
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            {
                "msg": "user created",
                "user": CustomUserSerializer(user).data,
                "tokens": get_tokens_for_user(user),
            },
            status=status.HTTP_201_CREATED,
        )

    except ValueError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )


# Manual login if JWT not present
@api_view(["POST"])
@permission_classes([AllowAny])
def manual_login(request):
    user_password = request.data.get("password")
    user_user_name = request.data.get("user_name")
    remember = request.data.get("remember")

    try:
        user = CustomUser.objects.get(user_name=user_user_name)
        if user.check_password(user_password):
            return choose_dashboard(
                user, tokens=get_tokens_for_user(user), remember=remember
            )
        else:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# Login view: prefer JWT, fallback to manual login
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    remember = False

    try:

        user_auth = JWTAuthentication().authenticate(request)
        if not user_auth:
            return Response(
                {"error": "JWT is not ok"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        else:
            user, _ = user_auth
            return choose_dashboard(user, tokens=None, remember=False)

    except AuthenticationFailed:
        return Response(
            {"error": "JWT is not ok"},
            status=status.HTTP_400_BAD_REQUEST,
        )
