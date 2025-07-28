from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
persian_validator = RegexValidator(
    regex=r'^[\u0600-\u06FF\s\u200c]+$',
    message="فقط حروف فارسی مجاز است."
)

english_validator = RegexValidator(
    regex=r'^[A-Za-z0-9@._\-*]+$',
    message="فقط حروف، اعداد و نمادهای @ . _ - * مجاز هستند."
)

phone_validator = RegexValidator(
    regex=r"^989\d{2}\s*?\d{3}\s*?\d{4}$", message=_("Invalid phone number."),
)
