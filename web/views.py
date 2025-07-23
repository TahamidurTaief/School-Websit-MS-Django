from django.shortcuts import render
import json

def home(request):
    dummy_data = {
        'notice': [
            {'date': '২৫ জানুয়ারি ২০২০', 'title': 'নোটিশ এক', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '২৫ জানুয়ারি ২০২০', 'title': 'নোটিশ দুই', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '২৫ জানুয়ারি ২০২০', 'title': 'নোটিশ তিন', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '২৫ জানুয়ারি ২০২০', 'title': 'নোটিশ চার', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '১ জানুয়ারি ২০২০', 'title': 'নোটিশ পাঁচ', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '২ জানুয়ারি ২০২০', 'title': 'নোটিশ ছয়', 'download_url': '#', 'icon': 'fa-file-pdf'},
        ],
        'results': [
            {'date': '২৫ জানুয়ারি ২০২০', 'title': 'ফলাফল এক', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '২৫ জানুয়ারি ২০২০', 'title': 'ফলাফল দুই', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '২৫ জানুয়ারি ২০২০', 'title': 'ফলাফল তিন', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '২৫ জানুয়ারি ২০২০', 'title': 'ফলাফল চার', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '১ জানুয়ারি ২০২০', 'title': 'ফলাফল পাঁচ', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '২ জানুয়ারি ২০২০', 'title': 'ফলাফল ছয়', 'download_url': '#', 'icon': 'fa-file-pdf'},
        ],
        'admission': [
            {'date': '২৫ জানুয়ারি ২০২০', 'title': 'ভর্তি এক', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '২৫ জানুয়ারি ২০২০', 'title': 'ভর্তি দুই', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '২৫ জানুয়ারি ২০২০', 'title': 'ভর্তি তিন', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '২৫ জানুয়ারি ২০২০', 'title': 'ভর্তি চার', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '১ জানুয়ারি ২০২০', 'title': 'ভর্তি পাঁচ', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '২ জানুয়ারি ২০২০', 'title': 'ভর্তি ছয়', 'download_url': '#', 'icon': 'fa-file-pdf'},
        ],
        'routine': [
            {'date': '২৫ জানুয়ারি ২০২০', 'title': 'রুটিন এক', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '২৫ জানুয়ারি ২০২০', 'title': 'রুটিন দুই', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '২৫ জানুয়ারি ২০২০', 'title': 'রুটিন তিন', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '২৫ জানুয়ারি ২০২০', 'title': 'রুটিন চার', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '১ জানুয়ারি ২০২০', 'title': 'রুটিন পাঁচ', 'download_url': '#', 'icon': 'fa-file-pdf'},
            {'date': '২ জানুয়ারি ২০২০', 'title': 'রুটিন ছয়', 'download_url': '#', 'icon': 'fa-file-pdf'},
        ],
    }
    
    # Convert the data to JSON for the template
    dummy_data_json = json.dumps(dummy_data)

    gallery_images = [
        '/static/img/home/institute.jpg',
        '/static/img/home/principal.jpg',
        '/static/img/home/slider1.jpg',
        '/static/img/home/slider2.jpg',
        '/static/img/home/slider3.jpg',
        '/static/img/home/institute.jpg',
        '/static/img/home/principal.jpg',
        '/static/img/home/slider1.jpg',
        '/static/img/home/slider2.jpg',
        '/static/img/home/slider3.jpg',
        
    ]
    
    return render(request, 'website/home.html', {
        'dummy_data': dummy_data,
        'dummy_data_json': dummy_data_json,
        'gallery_images': gallery_images,
    })