from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _


def clean_email(value):
    email = value
    if ".edu" in email:
        raise ValidationError("WE DO NOT ACCEPT EDU")


CATEGORIES = ['Mexican', 'Iranian', 'Asian', 'Chinese', 'Turkish', 'Italian']


def validate_category(value):
    cat = value.capitalize()
   # if value not in CATEGORIES and cat not in CATEGORIES:
      #  raise ValidationError(f"{value} not a valid category!")
