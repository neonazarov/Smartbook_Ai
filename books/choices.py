from django.db import models


class LanguageTypeChoice(models.TextChoices):
    uz = 'uz', 'Uz'
    ru = 'ru', 'Ru'
    en = 'en', 'En'