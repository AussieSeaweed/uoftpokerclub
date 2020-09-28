from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].required = True

    class Meta(UserCreationForm.Meta):
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
