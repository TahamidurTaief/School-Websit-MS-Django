from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

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
    path('results/', result_list, name='result_list'),
    path('filter-results/', filter_results, name='filter_results'),
    path('download-result/<int:pk>/', download_result, name='download_result'),
    path('view-result-pdf/<int:pk>/', view_result_pdf, name='view_result_pdf'),
    path('gallery/', gallery_list, name='gallery_list'),
    path('filter-gallery-images/', filter_gallery_images, name='filter_gallery_images'),
    path('filter-gallery-videos/', filter_gallery_videos, name='filter_gallery_videos'),
    path('information-service/', information_service, name='information_service'),
    path('filter-facilities/', filter_facilities, name='filter_facilities'),
    path('contact/', contact, name='contact'),
    path('contact/submit/', submit_contact_message, name='submit_contact_message'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    