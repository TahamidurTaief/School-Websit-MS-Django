from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('administration/', administration, name='administration'),
    path('students/', students, name='students'),
    path('filter/', filter_students, name='filter_students'),
    path('books/', books, name='books'),
    path('filter-books/', filter_books, name='filter_books'),
    path('routine/', routine, name='routine'),
    path('filter-routines/', filter_routines, name='filter_routines'),
    path('download-routine/<int:pk>/', download_routine, name='download_routine'),
    path('download-book/<int:pk>/', download_book, name='download_book'),

]