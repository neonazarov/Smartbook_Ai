import json
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from books.models import Book, Category
from users.models import Wishlist

from django.db.models import Q

from utils.ai import get_gpt_response


# Create your views here.
def home(request):
    q = request.GET.get('q')
    if q:
        books = Book.objects.filter(
            Q(title__icontains=q) |
            Q(author__first_name__icontains=q) |
            Q(author__last_name__icontains=q)
        ).order_by('-created_at')
    else:
        books = Book.objects.all().order_by('-created_at')
    wishlists = Wishlist.objects.filter(user=request.user).order_by('-created_at')[:3]
    print(wishlists)
    context = {
        "books": books,
        "wishlists": wishlists
    }
    return render(request, 'books/main.html', context=context)


def wishlist(request):
    wishlists = Wishlist.objects.filter(user=request.user).order_by('-created_at')
    context = {
        "wishlists": wishlists
    }
    return render(request, 'books/wishlist.html', context=context)

def add_to_wishlist(request, book_id):
    book = Book.objects.get(id=book_id)
    try:
        Wishlist.objects.create(user=request.user, book=book)
    except IntegrityError:
        wishlist = Wishlist.objects.get(user=request.user, book=book)
        wishlist.delete()
    return redirect(request.META.get('HTTP_REFERER', 'books:home'))


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    related_books = Book.objects.filter(
        categories__in=book.categories.all()
    ).exclude(id=book.id).distinct()
    context = {
        "book": book,
        "related_books": related_books
    }
    return render(request, 'books/details.html', context=context)

def recommendation(request):
    wishlist_books = Book.objects.filter(wishlist__user=request.user)
    user_preferred_categories = Category.objects.filter(books__in=wishlist_books).values_list('name', flat=True).distinct()
    if not user_preferred_categories:
        response = []
    else:

        prompt = f"""
            Based on the following user preferences, recommend 5 books. 
            Return the data as a JSON array of dictionaries with keys: title, author, genre, summary, cover_url so I use in python
            If no real image URL is available, use 'https://example.com/cover.jpg'.

            User preferences: {user_preferred_categories}
            """
        response = get_gpt_response(prompt=prompt)

    context = {
        "response": json.loads(response)
    }
    return render(request, 'books/recommendation.html', context=context)