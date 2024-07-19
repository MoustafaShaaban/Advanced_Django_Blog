import datetime
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, DateField, ImageField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for docker_blog_backend.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    date_of_birth = DateField(_("User Date of Birth"), blank=True, default=datetime.date.today)
    avatar = ImageField(_("User Avatar"), upload_to="users_avatar", default="default.jpg")
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
