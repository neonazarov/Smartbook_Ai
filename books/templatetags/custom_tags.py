from django import template
from django.contrib.auth import get_user_model
from books.models import Book
from users.models import Wishlist

register = template.Library()

@register.simple_tag(takes_context=True)
def is_in_wishlist(context, book_id):
    request = context['request']
    if not request.user.is_authenticated:
        return False
    book = Book.objects.get(id=book_id)

    return Wishlist.objects.filter(user=request.user, book=book).exists()

@register.filter
def dot_thousands(value):
    try:
        return "{:,.0f}".format(value).replace(",", ".")
    except (ValueError, TypeError):
        return value