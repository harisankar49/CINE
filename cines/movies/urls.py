from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),  # Corrected the name of the view function
    path('add_movie/', views.add_movie, name='add_movie'),
    path('movies/edit_movie/<int:id>/', views.edit_movie, name='edit_movie'),
    path('delete_movie/<int:id>/', views.delete_movie, name='delete_movie'),
    path('<int:c_id>/', views.allmoviescat, name='allmoviescat'),
    path('<int:c_id>/<int:p_id>/', views.home, name='home'),
    path('<int:c_id>/<int:p_id>/add-review/', views.add_review, name='add_review'),
path('add_category/', views.add_category, name='add_category'),
    path('', views.allmoviescat, name='allmoviescat'),
    # Default view without category ID
]