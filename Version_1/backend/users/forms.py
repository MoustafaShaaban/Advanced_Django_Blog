from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email")