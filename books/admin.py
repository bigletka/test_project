from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Author, Book, Favourite, Genre, Review, User


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'genre', 'publication_date')
    list_filter = ('author', 'genre', 'publication_date')
    search_fields = ('title', 'author__name', 'genre__name')
    date_hierarchy = 'publication_date'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'author', 'rating', 'text')
    list_filter = ('book', 'author', 'rating')
    search_fields = ('book__title', 'author__email')


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book')
    list_filter = ('user', 'book')
    search_fields = ('user__email', 'book__title')


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff',
                                      'is_superuser')}),
        (('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    # Remove references to 'groups' and 'user_permissions'
    filter_horizontal = ()
    list_filter = ('is_staff', 'is_superuser', 'is_active')
