from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    Group,
    Permission,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, id_code):
        return self.get(id_code=id_code)

    def create_student(
        self,
        first_name=None,
        last_name=None,
        user_type="student",
        password=None,
        id_code=None,
        active_mode=True,
        ed_class=None,
        **extra_fields,
    ):
        if not first_name:
            raise ValueError("The 'first_name' must be set")
        elif not last_name:
            raise ValueError("The 'last_name' must be set")
        elif not id_code:
            raise ValueError("The 'id_code' must be set")
        elif not password:
            raise ValueError("The 'password' must be set")
        elif not ed_class:
            raise ValueError("The 'ed_class' must be set")

        if self.model.objects.filter(id_code=id_code).exists():
            raise ValueError(f"The 'id_code' {id_code} is already taken.")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            id_code=id_code,
            active_mode=active_mode,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_teacher(
        self,
        first_name=None,
        last_name=None,
        user_type="teacher",
        password=None,
        id_code=None,
        active_mode=True,
        **extra_fields,
    ):
        if not first_name:
            raise ValueError("The 'first_name' must be set")
        elif not last_name:
            raise ValueError("The 'last_name' must be set")
        elif not id_code:
            raise ValueError("The 'id_code' must be set")
        elif not password:
            raise ValueError("The 'password' must be set")

        if self.model.objects.filter(id_code=id_code).exists():
            raise ValueError(f"The 'id_code' {id_code} is already taken.")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            id_code=id_code,
            active_mode=active_mode,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    USER_TYPES = [
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("admin", "Admin"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_code = models.PositiveIntegerField(unique=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPES, default="student")
    ed_class = models.ForeignKey(
        to="Ed_Class",
        on_delete=models.CASCADE,
        related_name="students",
        null=True,
        blank=True,
    )
    active_mode = models.BooleanField(default=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="customuser_set",
        related_query_name="customuser",
    )

    def get_by_natural_key(self, id_code):
        return self.get(id_code=id_code)

    objects = CustomUserManager()
    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Ed_Class(models.Model):
    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True,
    )
    teacher = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name="classes",
        null=False,
        blank=False,
    )


class Score(models.Model):
    title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )
    value = models.DecimalField(
        decimal_places=2,
        max_digits=3,
        null=False,
        blank=False,
    )
    student = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="scores",
    )
