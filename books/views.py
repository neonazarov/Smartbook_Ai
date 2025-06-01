import json
import random
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from books.models import Book, Category
from users.models import Wishlist

from django.db.models import Q

from utils.ai import get_gpt_response


# Create your views here.
def home(request):
    q = request.GET.get('q')
    recommended_book = request.session.get('recommended_book')
    print('session data: ', recommended_book)
    if q:
        books = Book.objects.filter(
            Q(title__icontains=q) |
            Q(author__first_name__icontains=q) |
            Q(author__last_name__icontains=q)
        ).order_by('-created_at')
    else:
        books = Book.objects.all().order_by('-created_at')
    wishlists = Wishlist.objects.filter(user=request.user).order_by('-created_at')[:3]
    context = {
        "books": books,
        "wishlists": wishlists,
        "recommended_book": recommended_book
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
    user_prompt = request.POST.get('prompt')
    wishlist_books = Book.objects.filter(wishlist__user=request.user)

    if not wishlist_books:
        context = {
            "response": []
        }
        return render(request, 'books/recommendation.html', context=context)

    if not wishlist_books.exists():
        response = []
    else:
        books_info = [
            {
                "title": book.title,
                "author": book.author.full_name,
                "genre": [category.name for category in book.categories.all()],
                "summary": book.description
            }
            for book in wishlist_books
        ]

        prompt = f"""
            Based on the following books a user liked, recommend 5 similar books. 
            Do not limit by genre. Instead, focus on writing style, themes, and content similarity.
            Return the results as a JSON array of dictionaries with the following keys: 
            "title", "author", "genre" (as an array of strings), "summary", "cover_url", movie_name (if exists).
            Only use real, working cover_url from public sites !!!.
            If not available, use 'https://example.com/cover.jpg'.

            User liked books: {json.dumps(books_info, indent=2)}
        """
    if user_prompt:
        default_prompt = """
            Return the results as a JSON array of dictionaries with the following keys: 
            "title", "author", "genre" (as an array of strings), "summary", "cover_url", movie_name (if exists).
            Only use real, working cover_url from public sites !!!.
            If not available, use 'https://example.com/cover.jpg'.
        """
        prompt = user_prompt + default_prompt
    response = get_gpt_response(prompt=prompt)
    data = json.loads(response)
    # Choose one random book and store it in the session
    if response:
        print(response)
        print("Storing in recommended_book")
        random_book = random.choice(data)
        print("RANDOM BOOK", random_book)
        request.session['recommended_book'] = random_book

    context = {
        "response": data if response else []
    }
    return render(request, 'books/recommendation.html', context=context)