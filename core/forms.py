from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm


class UserChangeForm(DjangoUserChangeForm):
    pass

    class Meta(DjangoUserChangeForm.Meta):
        pass


class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        fields = "username", "first_name", "last_name"
