from django.urls import path
from . import views

urlpatterns = [
    # Create a new user account
    # Method: POST
    # URL: /api/auth/signup/
    # Body (JSON): { "user_name": str, "password": str, "first_name": str (optional), "last_name": str (optional) }
    # Auth: AllowAny
    # Success: HTTP 201, { "msg": "user created", "user": {...}, "tokens": { "access": "...", "refresh": "..." } }
    # Error cases: 400 / 403 with {"error": "..."}
    path("signup/", views.signup, name="signup"),

    # Manual login (username + password)
    # Method: POST
    # URL: /api/auth/manual-login/
    # Body (JSON): { "user_name": str, "password": str, "remember": true|false }
    # Auth: AllowAny
    # Behavior: server returns tokens in response only if remember indicates so (see choose_dashboard)
    # Success: HTTP 200, { "success": "...", "user": {...}, ["tokens": {...}] }
    # Error cases: 404 / 401 with {"error": "..."}
    path("manual-login/", views.manual_login, name="manual_login"),

    # Login by JWT (preferred when client already has a JWT access token)
    # Method: POST
    # URL: /api/auth/login/
    # Headers: Authorization: Bearer <access_token>
    # Auth: AllowAny (view uses JWTAuthentication manually)
    # Success: HTTP 200, { "success": "...", "user": {...} }  (no tokens are returned here)
    # Error cases: 400 with {"error": "JWT is not ok"}
    path("login/", views.login, name="login"),
]
