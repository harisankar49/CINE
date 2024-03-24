from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.utils.text import slugify

from .forms import UserRegistrationForm, UserEditForm, MovieForm,CategoryForm
from .models import CustomUser, Movie, Category, Review
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseBadRequest

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "username already exist")
                return redirect('movies:register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already registered')
                return redirect('movies:register')
            else:
                user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                                last_name=last_name, email=email)
                user.save()
                messages.info(request, 'user created')
                print("User created")
                return redirect('movies:login')
        else:
            messages.info(request, "password mismatches")
            print("password mismatches")
            return redirect('movies:register')
    return render(request, 'register.html')

def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect(reverse('movies:profile'))  # Update to use reverse with namespace
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})
def profile(request):
    return render(request, 'profile.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('movies:allmoviescat')
        else:
            messages.info(request, 'Invalid credentials')
            print("invalid credentials")
            return redirect('movies:login')
    return render(request, 'login.html')

def allmoviescat(request, c_id=None):
    category_page = None
    movie_list = Movie.objects.all()

    if c_id is not None:
        category_page = get_object_or_404(Category, id=c_id)
        movie_list = Movie.objects.filter(category=category_page)

    paginator = Paginator(movie_list, 6)
    page = request.GET.get('page')

    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'category': category_page, 'movies': movies})

def home(request, c_id, p_id):
    movie = get_object_or_404(Movie, id=p_id)
    category = get_object_or_404(Category, id=c_id)
    return render(request, 'movie.html', {'movie': movie, 'category': category})

def add_review(request, c_id, p_id):
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')
        movie = get_object_or_404(Movie, id=p_id)
        Review.objects.create(movie=movie, user=request.user, rating=rating, comment=comment)
        return redirect('movies:home', c_id=c_id, p_id=p_id)
    return JsonResponse({'success': False})


def add_movie(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        actors = request.POST.get('actors')
        category_id = request.POST.get('category')  # Change category to category_id
        trailer_link = request.POST.get('trailer_link')
        image = request.FILES.get('image')
        release_date = request.POST.get('release_date')

        # Automatically generate the slug from the movie name
        slug = slugify(name)

        # Get the current user for the "Added by" field
        added_by = request.user

        # Create the movie object
        movie = Movie.objects.create(
            name=name,
            slug=slug,
            description=description,
            actors=actors,
            category_id=category_id,  # Change category to category_id
            trailer_link=trailer_link,
            image=image,
            release_date=release_date,
            added_by=added_by
        )

        # Redirect to the home page
        return redirect('movies:allmoviescat')

    else:
        # Fetch the list of categories
        categories = Category.objects.all()
        return render(request, 'add_movie.html', {'categories': categories})
def edit_movie(request, id):
    movie = get_object_or_404(Movie, id=id, added_by=request.user)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movie updated successfully.')
            return redirect('movies:allmoviescat')
    else:
        form = MovieForm(instance=movie)
    return render(request, 'edit_movie.html', {'form': form})

def delete_movie(request, id):
    movie = get_object_or_404(Movie, id=id)

    if request.method == 'POST':
        movie.delete()
        messages.success(request, 'Movie deleted successfully.')
        return redirect('movies:allmoviescat')

    return render(request, 'delete_movie.html', {'movie': movie})

def user_logout(request):
    logout(request)
    return redirect('movies:allmoviescat')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to a specific URL after successfully adding the category
            return redirect('movies:allmoviescat')  # Change 'success_url' to the appropriate URL
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})