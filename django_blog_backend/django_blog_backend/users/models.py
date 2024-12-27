import datetime
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, DateField, ImageField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for Django Blog Backend.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = CharField(_("First Name of User"), blank=True, max_length=255)  # type: ignore[assignment]
    last_name = CharField(_("Last Name of User"), blank=True, max_length=255)  # type: ignore[assignment]
    date_of_birth = DateField(_("User Date of Birth"), blank=True, default=datetime.date.today)
    avatar = ImageField(_("User Avatar"), upload_to="users_avatar", default="default.jpg")
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
