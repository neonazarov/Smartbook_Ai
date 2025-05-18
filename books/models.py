from django.db import models

from books.choices import LanguageTypeChoice
from config.models import BaseModel

# Create your models here.


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Author(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class Book(BaseModel):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    categories = models.ManyToManyField(Category, related_name='books')
    description = models.TextField(blank=True, null=True)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cover_image = models.ImageField(upload_to='covers', null=True, blank=True)
    pages = models.PositiveIntegerField()
    rating = models.FloatField(default=1.0)
    language = models.CharField(
        max_length=12, choices=LanguageTypeChoice.choices,
        default=LanguageTypeChoice.uz.value)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"