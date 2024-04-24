from django.core.exceptions import ValidationError


class PasswordCharacterValidation:
    special_chars = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    valid_types = 4

    def __init__(self, code):
        self.code = code

    def validate(self, password, user=None):
        if not self.is_password_strong(password):
            raise ValidationError(self.get_help_text(), code=self.code)

    def is_password_strong(self, password):
        types = self.get_types()

        for char in password:
            if char.isdigit():
                types["number"] = True
            elif char.islower():
                types["lowercase"] = True
            elif char.isupper():
                types["uppercase"] = True
            elif char in self.special_chars:
                types["symbol"] = True

        return len([t for t in types.values() if t]) >= self.valid_types

    def get_help_text(self):
        warn = ", ".join(self.get_types().keys())
        return f"Your password must contain at least {self.valid_types} of character types: {warn}."

    def get_types(self):
        types = {
            "symbol": False,
            "lowercase": False,
            "uppercase": False,
            "number": False,
        }
        return types
