from django.http import FileResponse, HttpResponseNotFound, HttpResponseServerError, JsonResponse
from django.shortcuts import render
import json
from .models import *
from urllib.parse import quote
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _
import os


def home(request):
    # Slider images (only with actual images)
    slider_images = Gallery.objects.filter(is_slider=True).exclude(image='').order_by('created_at')
    # School info (brief/history)
    school_info = SchoolInfo.objects.first()
    # All active principal/head/vice messages (with their roles)
    principal_messages = PrincipalMessage.objects.filter(is_active=True).select_related('role').order_by('order', '-created_at')
    # Notices, Results, Admission, Routine (latest 5 each)
    notices = Notice.objects.filter(type='notice', is_active=True).order_by('-date')[:5]
    results = Notice.objects.filter(type='result', is_active=True).order_by('-date')[:5]
    admissions = Notice.objects.filter(type='admission', is_active=True).order_by('-date')[:5]
    routines = Notice.objects.filter(type='routine', is_active=True).order_by('-date')[:5]
    # Recent event images (latest 6, only with actual images)
    event_images = Gallery.objects.filter(category='event').exclude(image='').order_by('-created_at')[:6]
    # Important links
    important_links = ImportantLink.objects.filter(is_active=True).order_by('order', '-created_at')
    # News items (latest 5)
    news_items = News.objects.filter(is_active=True).order_by('order', '-created_at')[:5]
    # News and Links section
    news_links_section = NewsLink.objects.filter(is_active=True).first()

    context = {
        'slider_images': slider_images,
        'school_info': school_info,
        'principal_messages': principal_messages,
        'notices': notices,
        'results': results,
        'admissions': admissions,
        'routines': routines,
        'event_images': event_images,
        'important_links': important_links,
        'news_items': news_items,
        'news_links_section': news_links_section,
    }
    return render(request, 'website/home.html', context)



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


from django.http import JsonResponse

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
    
    # Prepare data for JSON response
    routines_data = []
    for routine in routines:
        routines_data.append({
            'id': routine.id,
            'title': routine.title,
            'class_name': routine.class_name.name if routine.class_name else '',
            'department': routine.department.name if routine.department else '',
            'updated_at': routine.updated_at.strftime('%d %b %Y'),
            'file_url': routine.file.url,
            'download_url': f'/download-routine/{routine.id}/'
        })
        
    return JsonResponse({'routines': routines_data})




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
    
    if class_id and class_id.isdigit():
        books = books.filter(class_name_id=int(class_id))
    elif dept_slug:
        books = books.filter(department__slug=dept_slug)
    
    books = books.order_by('-updated_at')
    
    # Prepare data for JSON response
    books_data = []
    for book in books:
        books_data.append({
            'id': book.id,
            'title': book.title,
            'class_name': book.class_name.name if book.class_name else '',
            'department': book.department.name if book.department else '',
            'updated_at': book.updated_at.strftime('%d %b %Y'),
            'file_url': request.build_absolute_uri(book.file.url),
            'download_url': request.build_absolute_uri(f'/download-book/{book.id}/')
        })
        
    return JsonResponse({'books': books_data})


def download_book(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        file_path = book.file.path
        # Ensure the file exists before attempting to open
        if not os.path.exists(file_path):
            return HttpResponseNotFound('The requested file was not found.')

        response = FileResponse(open(file_path, 'rb'), as_attachment=True, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{quote(book.file.name)}"'
        return response
    except Book.DoesNotExist:
        return HttpResponseNotFound('Book not found.')
    except Exception as e:
        # Log the exception for debugging
        print(f"Error downloading book: {e}")
        return HttpResponseServerError('An error occurred during download.')

def result_list(request):
    classes = Class.objects.all().order_by('numeric_value')
    departments = Department.objects.all()

    context = {
        'classes': classes,
        'departments': departments,
    }
    return render(request, 'website/results.html', context)

def filter_results(request):
    class_id = request.GET.get('class_id')
    dept_slug = request.GET.get('dept_slug')

    results = Result.objects.filter(is_active=True)

    if class_id and class_id.isdigit():
        results = results.filter(class_name_id=int(class_id))
    elif dept_slug:
        results = results.filter(department__slug=dept_slug)

    results = results.order_by('-created_at')

    results_data = []
    for result in results:
        results_data.append({
            'id': result.id,
            'title': result.title,
            'class_name': result.class_name.name if result.class_name else '',
            'department': result.department.name if result.department else '',
            'updated_at': result.updated_at.strftime('%d %b %Y'),
            'file_url': result.file.url,
            'download_url': f'/download-result/{result.id}/',
        })

    return JsonResponse({'results': results_data})

def download_result(request, pk):
    try:
        result = Result.objects.get(pk=pk)
        file_path = result.file.path
        if not os.path.exists(file_path):
            return HttpResponseNotFound('The requested file was not found.')

        response = FileResponse(open(file_path, 'rb'), as_attachment=True, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{quote(result.file.name)}"'
        return response
    except Result.DoesNotExist:
        return HttpResponseNotFound('Result not found.')
    except Exception as e:
        print(f"Error downloading result: {e}")
        return HttpResponseServerError('An error occurred during download.')

def view_result_pdf(request, pk):
    result = Result.objects.get(pk=pk)
    response = FileResponse(result.file.open(), content_type='application/pdf')
    return response

def gallery_list(request):
    context = {
        'image_categories': Gallery.CATEGORIES,
    }
    return render(request, 'website/gallery.html', context)

def filter_gallery_images(request):
    category = request.GET.get('category', 'all')
    
    images = Gallery.objects.filter(is_slider=False) # Exclude sliders from main gallery

    if category != 'all':
        images = images.filter(category=category)

    images = images.order_by('-created_at')

    images_data = []
    for image in images:
        image_url = ''
        if image.image:
            image_url = request.build_absolute_uri(image.image.url)
        
        images_data.append({
            'id': image.id,
            'title': image.title,
            'image_url': image_url,
            'description': image.description,
            'category': image.get_category_display(),
        })
    return JsonResponse({'images': images_data})

def filter_gallery_videos(request):
    videos = Video.objects.filter(is_active=True).order_by('-created_at')

    videos_data = []
    for video in videos:
        videos_data.append({
            'id': video.id,
            'title': video.title,
            'youtube_id': video.youtube_id,
            'description': video.description,
        })
    return JsonResponse({'videos': videos_data})


def information_service(request):
    """Information Service Center page"""
    # Get slider images
    slider_images = InformationSlider.objects.filter(is_active=True).order_by('order')
    
    # If no slider images, create a default one
    if not slider_images.exists():
        slider_images = [InformationSlider(
            title='তথ্য সেবা কেন্দ্র',
            description='আমাদের প্রতিষ্ঠানের সকল তথ্য একসাথে',
            order=1,
            is_active=True
        )]
    
    # Get all facility information
    facilities = FacilityInfo.objects.filter(is_active=True).order_by('order')
    
    # Group facilities by type
    facility_groups = {}
    for facility in facilities:
        if facility.facility_type not in facility_groups:
            facility_groups[facility.facility_type] = []
        facility_groups[facility.facility_type].append(facility)
    
    # Get faculty information
    faculty_members = FacultyInfo.objects.filter(is_active=True).order_by('order')
    
    # Get information service content
    info_service = InformationService.objects.filter(is_active=True).first()
    
    context = {
        'slider_images': slider_images,
        'facility_groups': facility_groups,
        'faculty_members': faculty_members,
        'info_service': info_service,
    }
    return render(request, 'website/information_service.html', context)


def filter_facilities(request):
    """AJAX endpoint for filtering facilities"""
    facility_type = request.GET.get('type', 'all')
    
    facilities = FacilityInfo.objects.filter(is_active=True)
    
    if facility_type != 'all':
        facilities = facilities.filter(facility_type=facility_type)
    
    facilities = facilities.order_by('order')
    
    facilities_data = []
    for facility in facilities:
        facilities_data.append({
            'id': facility.id,
            'type': facility.facility_type,
            'type_display': facility.get_facility_type_display(),
            'title': facility.title,
            'description': facility.description,
            'icon': facility.icon,
            'count': facility.count,
            'unit': facility.unit,
            'image_url': facility.image.url if facility.image else '',
        })
    
    return JsonResponse({'facilities': facilities_data})


def contact(request):
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    return render(request, 'website/contact.html', {
        'contact_info': contact_info
    })

@csrf_exempt
@require_POST
def submit_contact_message(request):
    import json
    data = json.loads(request.body.decode('utf-8'))
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()
    title = data.get('title', '').strip()
    message = data.get('message', '').strip()

    errors = {}
    if not name:
        errors['name'] = 'নাম আবশ্যক।'
    if not phone:
        errors['phone'] = 'ফোন নম্বর আবশ্যক।'
    if not title:
        errors['title'] = 'বার্তার শিরোনাম আবশ্যক।'
    if not message:
        errors['message'] = 'বার্তার বিবরণ আবশ্যক।'

    if errors:
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    ContactMessage.objects.create(
        name=name,
        phone=phone,
        title=title,
        message=message
    )
    return JsonResponse({'success': True, 'message': 'আপনার বার্তা সফলভাবে পাঠানো হয়েছে!'}, status=201)