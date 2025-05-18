from django.db import models

from config.models import BaseModel
from books.models import Book

from django.contrib.auth.models import User

# Create your models here.
class Wishlist(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'book']


