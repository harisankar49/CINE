from django.shortcuts import render,redirect
from movies.models import Category,Movie
from django.db.models import Q
# Create your views here.

def searchresult(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    movies = Movie.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category_id:
        movies = movies.filter(category_id=category_id)

    categories = Category.objects.all()  # Fetch all categories for filtering

    return render(request, 'search.html', {'query': query, 'movies': movies, 'categories': categories})