from django.http import FileResponse
from django.shortcuts import render
import json
from .models import *


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
    dummy_data_json = json.dumps(dummy_data, ensure_ascii=False)

    gallery_images = [
        'img/home/institute.jpg',
        'img/home/principal.jpg',
        'img/home/slider1.jpg',
        'img/home/slider2.jpg',
        'img/home/slider3.jpg',
        'img/home/institute.jpg',
        'img/home/principal.jpg',
        'img/home/slider1.jpg',
        'img/home/slider2.jpg',
        'img/home/slider3.jpg',
    ]
    
    # Principal message data for the home page
    principal_message = {
        'title': 'অধ্যক্ষের বাণী',
        'name': 'প্রফেসর মোঃ আবদুল করিম',
        'message': 'প্রিয় শিক্ষার্থীরা,\n\nজ্ঞান অর্জনের জন্য অধ্যবসায়, সততা ও নিষ্ঠার বিকল্প নেই। তোমাদের প্রতিটি দিন হোক নতুন কিছু শেখার এবং নিজেকে গড়ে তোলার। আমাদের প্রতিষ্ঠান তোমাদের স্বপ্নপূরণের সহযাত্রী।\n\nশিক্ষা শুধু ডিগ্রি নয়, এটি মানবিক মূল্যবোধ, নৈতিকতা ও নেতৃত্বের শিক্ষা। তোমরা দেশ ও জাতির গর্ব হয়ে উঠো, এই কামনা করি।\n\nধন্যবাদ।'
    }
    
    return render(request, 'website/home.html', {
        'dummy_data': dummy_data,
        'dummy_data_json': dummy_data_json,
        'gallery_images': gallery_images,
        'principal_message': principal_message,
    })



def administration(request):
    # Dummy data - will be replaced with database queries
    administration_data = {
        'special_officers': [
            {
                'name': 'জনাব আব্দুল করিম',
                'position': 'প্রধান অভিযোগ গ্রহণকারী কর্মকর্তা',
                'image': 'img/administration/1.jpeg',
                'social_links': [
                    {'url': '#', 'icon': 'fab fa-facebook-f', 'hover_color': 'text-blue-600'},
                    {'url': '#', 'icon': 'fab fa-twitter', 'hover_color': 'text-blue-400'},
                    {'url': '#', 'icon': 'fab fa-linkedin-in', 'hover_color': 'text-blue-700'}
                ]
            },
            {
                'name': 'জনাব রফিকুল ইসলাম',
                'position': 'সহকারী অভিযোগ গ্রহণকারী কর্মকর্তা',
                'image': 'img/administration/2.jpeg',
                'social_links': [
                    {'url': '#', 'icon': 'fab fa-facebook-f', 'hover_color': 'text-blue-600'},
                    {'url': '#', 'icon': 'fab fa-twitter', 'hover_color': 'text-blue-400'},
                    {'url': '#', 'icon': 'fab fa-linkedin-in', 'hover_color': 'text-blue-700'}
                ]
            },
            {
                'name': 'জনাব আমিনুল হক',
                'position': 'সহকারী অভিযোগ গ্রহণকারী কর্মকর্তা',
                'image': 'img/administration/3.jpeg',
                'social_links': [
                    {'url': '#', 'icon': 'fab fa-facebook-f', 'hover_color': 'text-blue-600'},
                    {'url': '#', 'icon': 'fab fa-twitter', 'hover_color': 'text-blue-400'},
                    {'url': '#', 'icon': 'fab fa-linkedin-in', 'hover_color': 'text-blue-700'}
                ]
            },
            {
                'name': 'জনাবা সালমা বেগম',
                'position': 'সহকারী অভিযোগ গ্রহণকারী কর্মকর্তা',
                'image': 'img/administration/4.jpeg',
                'social_links': [
                    {'url': '#', 'icon': 'fab fa-facebook-f', 'hover_color': 'text-blue-600'},
                    {'url': '#', 'icon': 'fab fa-twitter', 'hover_color': 'text-blue-400'},
                    {'url': '#', 'icon': 'fab fa-linkedin-in', 'hover_color': 'text-blue-700'}
                ]
            }
        ],
        'teachers': [
            {'name': 'ড. মোহাম্মদ আলী', 'position': 'প্রধান শিক্ষক', 'image': 'img/administration/10.jpeg'},
            {'name': 'জনাব রহিম উদ্দিন', 'position': 'সহকারী শিক্ষক', 'image': 'img/administration/9.jpg'},
            {'name': 'জনাবা ফারজানা আক্তার', 'position': 'সহকারী শিক্ষিকা', 'image': 'img/administration/8.jpeg'},
            {'name': 'জনাব কামাল হোসেন', 'position': 'সহকারী শিক্ষক', 'image': 'img/administration/7.jpeg'},
            {'name': 'জনাবা নাসরিন সুলতানা', 'position': 'সহকারী শিক্ষিকা', 'image': 'img/administration/6.jpeg'},
            {'name': 'জনাব মাহমুদুল হাসান', 'position': 'সহকারী শিক্ষক', 'image': 'img/administration/5.jpeg'},
            {'name': 'জনাবা সাবরিনা হক', 'position': 'সহকারী শিক্ষিকা', 'image': 'img/administration/4.jpeg'},
            {'name': 'জনাব তৌহিদুল ইসলাম', 'position': 'সহকারী শিক্ষক', 'image': 'img/administration/3.jpeg'},
            {'name': 'জনাবা রুমানা আক্তার', 'position': 'সহকারী শিক্ষিকা', 'image': 'img/administration/2.jpeg'},
            {'name': 'জনাব আরিফুল ইসলাম', 'position': 'সহকারী শিক্ষক', 'image': 'img/administration/1.jpeg'}
        ]
    }
    
    return render(request, 'website/administration.html', administration_data)




def students(request):
    classes = Class.objects.all().order_by('numeric_value')
    departments = Department.objects.all()
    
    initial_class = classes.first()
    students = Student.objects.filter(class_name=initial_class).select_related('class_name', 'department') if initial_class else []
    
    context = {
        'classes': classes,
        'departments': departments,
        'initial_students': students,
        'initial_class_id': initial_class.id if initial_class else None,
    }
    return render(request, 'website/students.html', context)

def filter_students(request):
    class_id = request.GET.get('class_id')
    dept_slug = request.GET.get('dept_slug')
    
    students = Student.objects.all().select_related('class_name', 'department')
    
    if class_id:
        students = students.filter(class_name_id=class_id)
    elif dept_slug:
        students = students.filter(department__slug=dept_slug)
    
    students_data = [{
        'id': student.id,
        'name': student.name,
        'roll': student.roll_number,
        'registration': student.registration_number,
        'class_name': student.class_name.name,
        'department': student.department.name if student.department else '',
        'image': student.photo.url if student.photo else f'/static/img/administration/{student.id % 10 + 1}.jpeg',
        'guardian_name': student.guardian_name,
        'guardian_phone': student.guardian_phone,
        'address': student.address,
    } for student in students]
    
    return render(request, 'component/students/student_list.html', {'students': students_data})






def about(request):
    # Sample about us content
    about_content = {
        'title': 'আমাদের সম্পর্কে (About Us)',
        'history': {
            'title': 'প্রতিষ্ঠানের ইতিহাস',
            'content': 'আমাদের স্কুল ১৯৮০ সালে প্রতিষ্ঠিত হয়েছিল। প্রতিষ্ঠানটি প্রথমে একটি ছোট ভবনে শুরু হয়েছিল মাত্র ৫০ জন শিক্ষার্থী নিয়ে। বর্তমানে আমাদের প্রতিষ্ঠানে ১০০০+ শিক্ষার্থী অধ্যয়নরত। গত ৪০+ বছরে আমাদের প্রতিষ্ঠান অনেক চড়াই-উতরাই পেরিয়ে আজ একটি সম্মানজনক অবস্থানে পৌঁছেছে। আমাদের প্রাক্তন শিক্ষার্থীরা দেশের বিভিন্ন গুরুত্বপূর্ণ পদে অধিষ্ঠিত আছেন এবং সমাজের উন্নয়নে অবদান রাখছেন।'
        },
        'brief_info': {
            'title': 'সংক্ষিপ্ত তথ্য',
            'teachers': '৫০+',
            'departments': '৫',
            'classrooms': '৩০+',
            'students': '১০০০+',
            'description': 'আমাদের প্রতিষ্ঠানে অভিজ্ঞ শিক্ষক-শিক্ষিকা দ্বারা পরিচালিত বিভিন্ন বিভাগ রয়েছে। আধুনিক সুযোগ-সুবিধা সম্পন্ন ক্লাসরুম, ল্যাবরেটরি, লাইব্রেরি এবং খেলার মাঠ রয়েছে।'
        },
        'principal_message': {
            'title': 'অধ্যক্ষের বাণী',
            'name': 'প্রফেসর মোঃ আবদুল করিম',
            'message': 'প্রিয় শিক্ষার্থীরা,\n\nজ্ঞান অর্জনের জন্য অধ্যবসায়, সততা ও নিষ্ঠার বিকল্প নেই। তোমাদের প্রতিটি দিন হোক নতুন কিছু শেখার এবং নিজেকে গড়ে তোলার। আমাদের প্রতিষ্ঠান তোমাদের স্বপ্নপূরণের সহযাত্রী।\n\nশিক্ষা শুধু ডিগ্রি নয়, এটি মানবিক মূল্যবোধ, নৈতিকতা ও নেতৃত্বের শিক্ষা। তোমরা দেশ ও জাতির গর্ব হয়ে উঠো, এই কামনা করি।\n\nধন্যবাদ।'
        },
        'approval': {
            'title': 'অনুমোদন',
            'content': 'আমাদের প্রতিষ্ঠানটি শিক্ষা মন্ত্রণালয় কর্তৃক অনুমোদিত এবর বাংলাদেশ শিক্ষা বোর্ড দ্বারা স্বীকৃত। আমাদের প্রতিষ্ঠানের সকল শাখা সরকারি নিয়ম অনুযায়ী পরিচালিত হয়।',
            'branches': [
                {'name': 'প্রধান শাখা', 'location': 'মিরপুর, ঢাকা', 'established': '১৯৮০'},
                {'name': 'দ্বিতীয় শাখা', 'location': 'উত্তরা, ঢাকা', 'established': '২০০৫'}
            ]
        },
        'recognition': {
            'title': 'স্বীকৃতি',
            'content': 'আমাদের প্রতিষ্ঠান বিভিন্ন জাতীয় ও আন্তর্জাতিক পুরস্কার অর্জন করেছে। আমরা শিক্ষা মন্ত্রণালয় থেকে "সেরা শিক্ষা প্রতিষ্ঠান" হিসেবে স্বীকৃতি পেয়েছি।'
        },
        'aims': {
            'title': 'লক্ষ্য ও উদ্দেশ্য',
            'content': 'আমাদের প্রতিষ্ঠানের মূল লক্ষ্য হল শিক্ষার্থীদের মেধা ও মননের সর্বাঙ্গীণ বিকাশ সাধন করা। আমরা চাই আমাদের শিক্ষার্থীরা শুধু একাডেমিক জ্ঞান নয়, বরং নৈতিক মূল্যবোধ, সামাজিক দায়বদ্ধতা এবং নেতৃত্বের গুণাবলী অর্জন করুক।',
            'points': [
                'উচ্চমানের শিক্ষা প্রদান',
                'নৈতিক মূল্যবোধ গঠন',
                'সৃজনশীলতা ও উদ্ভাবনী চিন্তার বিকাশ',
                'দেশপ্রেম ও সামাজিক দায়বদ্ধতা সৃষ্টি',
                'আধুনিক প্রযুক্তি ব্যবহারে দক্ষতা অর্জন'
            ]
        },
        'news_links': {
            'title': 'সংবাদ/প্রয়োজনীয় লিংক',
            'news': [
                {'title': 'বার্ষিক ক্রীড়া প্রতিযোগিতা ২০২৩', 'date': '১০ ডিসেম্বর, ২০২৩', 'link': '#'},
                {'title': 'বিজ্ঞান মেলা আয়োজন', 'date': '১৪ নভেম্বর, ২০২৩', 'link': '#'},
                {'title': 'শিক্ষক নিয়োগ বিজ্ঞপ্তি', 'date': '০৫ অক্টোবর, ২০২৩', 'link': '#'}
            ],
            'links': [
                {'title': 'শিক্ষা মন্ত্রণালয়', 'url': 'https://moedu.gov.bd/'},
                {'title': 'বাংলাদেশ শিক্ষা বোর্ড', 'url': 'https://www.educationboard.gov.bd/'},
                {'title': 'জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড', 'url': 'http://www.nctb.gov.bd/'}
            ]
        }
    }
    
    return render(request, 'website/about.html', {
        'about_content': about_content
    })






def routine(request):
    classes = Class.objects.all().order_by('numeric_value')
    departments = Department.objects.all()
    
    # Get initial routines (class routines by default)
    initial_routines = Routine.objects.filter(
        category='class', 
        is_active=True
    ).select_related('class_name', 'department')
    
    context = {
        'classes': classes,
        'departments': departments,
        'initial_routines': initial_routines,
    }
    return render(request, 'website/routine.html', context)


def filter_routines(request):
    routine_type = request.GET.get('type', 'class')
    class_id = request.GET.get('class_id')
    dept_slug = request.GET.get('dept_slug')
    
    routines = Routine.objects.filter(
        category=routine_type,
        is_active=True
    ).select_related('class_name', 'department')
    
    if class_id and class_id.isdigit():
        routines = routines.filter(class_name_id=int(class_id))
    elif dept_slug:
        routines = routines.filter(department__slug=dept_slug)
    
    routines = routines.order_by('-updated_at')
    
    return render(request, 'component/routine/routine_list.html', {
        'routines': routines
    })




def download_routine(request, pk):
    routine = Routine.objects.get(pk=pk)
    response = FileResponse(routine.file.open(), as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{routine.file.name}"'
    return response



def books(request):
    classes = Class.objects.all().order_by('numeric_value')
    departments = Department.objects.all()
    
    # Get initial books
    initial_books = Book.objects.filter(
        is_active=True
    ).select_related('class_name', 'department')
    
    context = {
        'classes': classes,
        'departments': departments,
        'initial_books': initial_books,
    }
    return render(request, 'website/books.html', context)




def filter_books(request):
    class_id = request.GET.get('class_id')
    dept_slug = request.GET.get('dept_slug')
    
    books = Book.objects.filter(
        is_active=True
    ).select_related('class_name', 'department')
    
    if class_id:
        books = books.filter(class_name_id=class_id)
    elif dept_slug:
        books = books.filter(department__slug=dept_slug)
    
    books = books.order_by('-updated_at')
    
    return render(request, 'component/routine/book_list.html', {
        'books': books
    })