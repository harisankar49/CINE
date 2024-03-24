from django.contrib import admin
from .models import Category, Movie

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'release_date', 'actors', 'category', 'trailer_link','image']
    list_editable = ['name', 'description', 'release_date', 'actors', 'category', 'trailer_link','image']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20
    list_display_links = None

admin.site.register(Movie, MovieAdmin)
