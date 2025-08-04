from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import CustomUser, Ed_Class
from .serializers import CustomUserDetailSerializer


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
                "user_type": user.user_type,
                "success": msg,
                "user": CustomUserDetailSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )
    else:
        if remember == True:
            return Response(
                {
                    "user_type": user.user_type,
                    "success": msg,
                    "tokens": tokens,
                    "user": CustomUserDetailSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "user_type": user.user_type,
                    "success": msg,
                    "user": CustomUserDetailSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )


# Admin-only signup view
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def signup(request):
    user_auth = JWTAuthentication().authenticate(request)
    if not user_auth:
        return Response(
            {"error": "your JWT is not fine"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user, _ = user_auth
    if user.user_type != "admin":
        return Response(
            {"error": "You're not allowed"}, status=status.HTTP_403_FORBIDDEN
        )

    # Extract new user data
    user_user_type = request.data.get("user_type")
    user_id_code = request.data.get("id_code")
    user_password = request.data.get("password")
    user_first_name = request.data.get("first_name")
    user_last_name = request.data.get("last_name")

    # Check for required fields
    if not all(
        [user_user_type, user_id_code, user_password, user_first_name, user_last_name]
    ):
        return Response(
            {
                "error": "All fields (user_type, id_code, password, first_name, last_name) are required."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        if user_user_type == "teacher":
            new_user = CustomUser.objects.create_teacher(
                id_code=user_id_code,
                password=user_password,
                first_name=user_first_name,
                last_name=user_last_name,
            )
        elif user_user_type == "student":

            student_class_title = request.data.get("student_class")
            if not student_class_title:
                return Response(
                    {"error": "'student_class is requirement'"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                student_class = Ed_Class.objects.get(title=student_class_title)
            except Ed_Class.DoesNotExist:
                return Response(
                    {"error": "'student_class' not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            new_user = CustomUser.objects.create_student(
                id_code=user_id_code,
                password=user_password,
                first_name=user_first_name,
                last_name=user_last_name,
                ed_class=student_class,
            )
        else:
            return Response(
                {"error": "Invalid user_type. Must be 'student' or 'teacher'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "message": "user created successfuly",
                "user": CustomUserDetailSerializer(new_user).data,
            },
            status=status.HTTP_201_CREATED,
        )

    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Manual login if JWT not present
def manual_login(request, remember):
    user_id_code = request.data.get("id_code")
    user_password = request.data.get("password")

    if not user_id_code or not user_password:
        return Response(
            {"error": "id_code and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = CustomUser.objects.get(id_code=user_id_code)
        if user.check_password(user_password):
            return choose_dashboard(
                user, tokens=get_tokens_for_user(user), remember=remember
            )
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# Login view: prefer JWT, fallback to manual login
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    remember = request.data.get("remember")
    if not remember:
        remember = False

    try:

        user_auth = JWTAuthentication().authenticate(request)
        if not user_auth:
            return manual_login(request, remember=remember)

        else:
            user, _ = user_auth
            return choose_dashboard(user, tokens=None, remember=False)

    except AuthenticationFailed:
        return manual_login(request, remember=remember)
