from django.contrib import admin

# models
from users.models import Wishlist

# Register your models here.
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'book',)