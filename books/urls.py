from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.home, name='home'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('details/<int:book_id>/', views.book_detail, name='detail'),
    path('add_to_wishlist/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('recommendation/', views.recommendation, name='recommendation')
]