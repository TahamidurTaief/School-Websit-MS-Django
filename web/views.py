# web/views.py

from django.http import FileResponse, HttpResponseNotFound, HttpResponseServerError, JsonResponse
from django.shortcuts import get_object_or_404, render
import json
from .models import *
from urllib.parse import quote
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _
import os
from .models import Teacher, FacultyMember
from django.urls import reverse




def home(request):
    slider_images = Slider.objects.filter(is_active=True).exclude(image='').order_by('-created_at')
    brief_info_obj = SchoolBriefInfo.objects.filter(is_active=True).first()
    school_history = SchoolHistory.objects.all().first()
    gallery_images = Gallery.objects.all().order_by('-created_at')[:12]
    principal_message = PrincipalMessage.objects.filter(
        is_active=True, 
        show_on_home_page=True
    ).select_related('role').first()
    
    # Fetch AboutMessage with serial_no=1 for home page
    message = AboutMessage.objects.filter(is_active=True, serial_no=1).first()

    # Data Fetching for Important Info
    notices = Notice.objects.filter(type='notice', is_active=True).order_by('-date')[:5]
    results = Notice.objects.filter(type='result', is_active=True).order_by('-date')[:5]
    admissions = Notice.objects.filter(type='admission', is_active=True).order_by('-date')[:5]
    routines = Notice.objects.filter(type='routine', is_active=True).order_by('-date')[:5]
    
    def format_notice_data(queryset, icon_class):
        return [
            {
                'icon': icon_class,
                'title': item.title,
                'date': item.date.strftime('%d %b, %Y'),
                'download_url': reverse('download_notice_file', kwargs={'pk': item.pk})
            }
            for item in queryset
        ]

    important_info_data = {
        'notice': format_notice_data(notices, 'fa-bell'),
        'results': format_notice_data(results, 'fa-chart-bar'),
        'admission': format_notice_data(admissions, 'fa-user-plus'),
        'routine': format_notice_data(routines, 'fa-calendar-alt'),
    }
    
    important_info_json = json.dumps(important_info_data)

    brief_info_context = {
        'title': brief_info_obj.title if brief_info_obj else 'সংক্ষিপ্ত তথ্য',
        'teachers': brief_info_obj.teachers_count if brief_info_obj else 'N/A',
        'departments': brief_info_obj.departments_count if brief_info_obj else 'N/A',
        'classrooms': brief_info_obj.classrooms_count if brief_info_obj else 'N/A',
        'students': brief_info_obj.students_count if brief_info_obj else 'N/A',
        'description': brief_info_obj.description if brief_info_obj else 'সংক্ষিপ্ত তথ্যের বিবরণ পাওয়া যায়নি।'
    }
    event_images = Gallery.objects.filter(category='event').exclude(image='').order_by('-created_at')[:6]
    important_links = ImportantLink.objects.filter(is_active=True).order_by('order', '-created_at')
    news_items = News.objects.filter(is_active=True).order_by('order', '-created_at')[:5]
    news_links_section = NewsLink.objects.filter(is_active=True).first()
    
    # Recent Events - Top 6 events for home page
    recent_events = EventAndNews.objects.filter(status=True).order_by('-created_at')[:6]

    context = {
        'slider_images': slider_images,
        'principal_message': principal_message,
        'message': message,
        'important_info_json': important_info_json,
        'event_images': event_images,
        'important_links': important_links,
        'news_items': news_items,
        'news_links_section': news_links_section,
        'brief_info': brief_info_context,
        'school_history': school_history,
        'recent_events': recent_events,
        'gallery_images' : gallery_images,
    }
    return render(request, 'website/home.html', context)


def download_notice_file(request, pk):
    """
    Handles the download of ANY file from the Notice model,
    whether it is a notice, result, routine, or admission file.
    """
    item = get_object_or_404(Notice, pk=pk)
    try:
        filename = quote(os.path.basename(item.file.name))
        response = FileResponse(item.file.open('rb'), as_attachment=True, filename=filename)
        return response
    except FileNotFoundError:
        return HttpResponseNotFound("The requested file was not found on the server.")
    except Exception as e:
        print(f"Error downloading notice file: {e}")
        return HttpResponseServerError("An error occurred while trying to download the file.")






def administration(request):
    slider_images = Slider.objects.filter(is_active=True).exclude(image='').order_by('-created_at')
    
    # Fetch from new FacultyMember model
    management_members = FacultyMember.objects.filter(category='management', is_active=True).order_by('order', 'id')
    teacher_members = FacultyMember.objects.filter(category='teacher', is_active=True).order_by('order', 'id')
    administration_members = FacultyMember.objects.filter(category='administration', is_active=True).order_by('order', 'id')
    staff_members = FacultyMember.objects.filter(category='staff', is_active=True).order_by('order', 'id')
    
    # Keep old Teacher model data for backward compatibility (if needed)
    special_officers = Teacher.objects.filter(category='special_officer').order_by('id')
    teachers = Teacher.objects.filter(category='teacher').order_by('id')
    management_board = Teacher.objects.filter(category='management_board').order_by('id')
    administration_officers = Teacher.objects.filter(category='administration').order_by('id')
    kormochari_members = Teacher.objects.filter(category='kormochari').order_by('id')

    administration_data = {
        # New FacultyMember data
        'management_members': management_members,
        'teacher_members': teacher_members,
        'administration_members': administration_members,
        'staff_members': staff_members,
        
        # Old Teacher model data (for backward compatibility)
        'special_officers': special_officers,
        'teachers': teachers,
        'management_board': management_board,
        'administration_officers': administration_officers,
        'kormochari_members': kormochari_members,
        'slider_images': slider_images,
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
    """Enhanced About page with modern UI elements from information service"""
    try:
        # === EXISTING ABOUT PAGE DATA ===
        # Get main about page configuration
        about_page = AboutPage.objects.filter(is_active=True).first()
        
        # Get school history
        history = SchoolHistory.objects.filter(is_active=True).first()
        
        # Get brief information
        brief_info = SchoolBriefInfo.objects.filter(is_active=True).first()
        
        # Get principal message for about page (deprecated - will be replaced by messages)
        principal_message_obj = AboutMessage.objects.filter(is_active=True).first()
        
        # Get all active messages for about page (excluding serial_no=1 which shows on home)
        messages = AboutMessage.objects.filter(is_active=True, serial_no__gt=1).order_by('serial_no')
        
        # Get school approval information
        approval = SchoolApproval.objects.filter(is_active=True).first()
        
        # Get school recognition
        recognition = SchoolRecognition.objects.filter(is_active=True).first()
        
        # Get school aims and objectives
        aims = SchoolAims.objects.filter(is_active=True).first()
        
        # Get aim points
        aim_points = []
        if aims:
            aim_points = AimPoint.objects.filter(aim=aims, is_active=True).order_by('order')
        
        # Get news items (using EventAndNews model)
        news_items = EventAndNews.objects.filter(status=True, type='NEWS').order_by('-created_at')[:5]
        
        # Get important links
        links = AboutLink.objects.filter(is_active=True).order_by('order')[:5]
        
        # === NEW: INFORMATION SERVICE DATA FOR MODERN UI ===
        # Get slider images (using main Slider model)
        slider_images = Slider.objects.filter(is_active=True).exclude(image='').order_by('-created_at')
        
        # Get all facility information for stats section
        facilities = FacilityInfo.objects.filter(is_active=True).order_by('order')
        
        # Group facilities by type for modern display
        facility_groups = {}
        for facility in facilities:
            if facility.facility_type not in facility_groups:
                facility_groups[facility.facility_type] = []
            facility_groups[facility.facility_type].append(facility)
        
        # Get faculty information for team section (use administration teachers only)
        faculty_members = FacultyMember.objects.filter(is_active=True, category='administration').order_by('order')[:8]  # Limit to 8 for about page
        
        # Get information service content
        info_service = InformationService.objects.filter(is_active=True).first()
        
        # Prepare context data
        about_content = {
            'title': about_page.title if about_page else 'আমাদের সম্পর্কে (About Us)',
            'history': {
                'title': history.title if history else 'প্রতিষ্ঠানের ইতিহাস',
                'content': history.content if history else 'ইতিহাসের তথ্য পাওয়া যায়নি।'
            },
            'brief_info': {
                'title': brief_info.title if brief_info else 'সংক্ষিপ্ত তথ্য',
                'teachers': brief_info.teachers_count if brief_info else '৫০+',
                'departments': brief_info.departments_count if brief_info else '৫',
                'classrooms': brief_info.classrooms_count if brief_info else '৩০+',
                'students': brief_info.students_count if brief_info else '১০০০+',
                'description': brief_info.description if brief_info else 'সংক্ষিপ্ত তথ্যের বিবরণ পাওয়া যায়নি।'
            },
            'principal_message': principal_message_obj,
            'approval': {
                'title': approval.title if approval else 'অনুমোদন',
                'content': approval.content if approval else 'অনুমোদনের তথ্য পাওয়া যায়নি।',
                'image': approval.image if approval else None
            },
            'recognition': recognition,
            'aims': {
                'title': aims.title if aims else 'লক্ষ্য ও উদ্দেশ্য',
                'content': aims.content if aims else 'লক্ষ্য ও উদ্দেশ্যের বিবরণ পাওয়া যায়নি।',
                'points': [point.point for point in aim_points]
            },
            'news_links': {
                'title': 'সংবাদ/প্রয়োজনীয় লিংক',
                'news': [
                    {
                        'title': news.title,
                        'date': news.created_at.strftime('%d %B, %Y') if news.created_at else 'তারিখ নেই',
                        'link': '#'  # Can be enhanced later with actual links
                    } for news in news_items
                ],
                'links': [
                    {
                        'title': link.title,
                        'url': link.url
                    } for link in links
                ]
            }
        }
        
        # Enhanced context with modern UI data
        context = {
            'about_content': about_content,
            'messages': messages,
            # === NEW: MODERN UI DATA ===
            'slider_images': slider_images,
            'facility_groups': facility_groups,
            'faculty_members': faculty_members,
            'info_service': info_service,
        }
        
        return render(request, 'website/about.html', context)
        
    except Exception as e:
        # Fallback to default content if there's any error
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
            'principal_message': None,
            'approval': {
                'title': 'অনুমোদন',
                'content': 'আমাদের প্রতিষ্ঠানটি শিক্ষা মন্ত্রণালয় কর্তৃক অনুমোদিত এবর বাংলাদেশ শিক্ষা বোর্ড দ্বারা স্বীকৃত। আমাদের প্রতিষ্ঠানের সকল শাখা সরকারি নিয়ম অনুযায়ী পরিচালিত হয়।',
                'branches': [
                    {'name': 'প্রধান শাখা', 'location': 'মিরপুর, ঢাকা', 'established': '১৯৮০'},
                    {'name': 'দ্বিতীয় শাখা', 'location': 'উত্তরা, ঢাকা', 'established': '২০০৫'}
                ]
            },
            'recognition': None,
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
            'about_content': about_content,
            'messages': []  # Empty list as fallback
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


def syllabus(request):
    classes = Class.objects.all().order_by('numeric_value')
    departments = Department.objects.all()
    
    # Get initial syllabus
    initial_syllabus = Syllabus.objects.filter(
        is_active=True
    ).exclude(file='').select_related('class_name', 'department')
    
    context = {
        'classes': classes,
        'departments': departments,
        'initial_syllabus': initial_syllabus,
    }
    return render(request, 'website/syllabus.html', context)


def filter_syllabus(request):
    class_id = request.GET.get('class_id')
    dept_slug = request.GET.get('dept_slug')
    
    syllabus_items = Syllabus.objects.filter(
        is_active=True
    ).exclude(file='').select_related('class_name', 'department')
    
    if class_id and class_id.isdigit():
        syllabus_items = syllabus_items.filter(class_name_id=int(class_id))
    elif dept_slug:
        syllabus_items = syllabus_items.filter(department__slug=dept_slug)
    
    syllabus_items = syllabus_items.order_by('-updated_at')
    
    # Prepare data for JSON response
    syllabus_data = []
    for syllabus in syllabus_items:
        syllabus_data.append({
            'id': syllabus.id,
            'title': syllabus.title,
            'class_name': syllabus.class_name.name if syllabus.class_name else '',
            'department': syllabus.department.name if syllabus.department else '',
            'updated_at': syllabus.updated_at.strftime('%d %b %Y'),
            'file_url': request.build_absolute_uri(syllabus.file.url) if syllabus.file else '',
            'download_url': request.build_absolute_uri(f'/download-syllabus/{syllabus.id}/')
        })
        
    return JsonResponse({'syllabus': syllabus_data})


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

def download_syllabus(request, pk):
    try:
        syllabus = Syllabus.objects.get(pk=pk)
        file_path = syllabus.file.path
        # Ensure the file exists before attempting to open
        if not os.path.exists(file_path):
            return HttpResponseNotFound('The requested file was not found.')

        response = FileResponse(open(file_path, 'rb'), as_attachment=True, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{quote(syllabus.file.name)}"'
        return response
    except Syllabus.DoesNotExist:
        return HttpResponseNotFound('Syllabus not found.')
    except Exception as e:
        # Log the exception for debugging
        print(f"Error downloading syllabus: {e}")
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


# Admission Views
def admission_list(request):
    classes = Class.objects.all().order_by('numeric_value')
    departments = Department.objects.all()

    context = {
        'classes': classes,
        'departments': departments,
    }
    return render(request, 'website/admissions.html', context)

def filter_admissions(request):
    class_id = request.GET.get('class_id')
    dept_slug = request.GET.get('dept_slug')

    admissions = Admission.objects.filter(is_active=True)

    if class_id and class_id.isdigit():
        admissions = admissions.filter(class_name_id=int(class_id))
    elif dept_slug:
        admissions = admissions.filter(department__slug=dept_slug)

    admissions = admissions.order_by('-created_at')

    admissions_data = []
    for admission in admissions:
        admissions_data.append({
            'id': admission.id,
            'title': admission.title,
            'class_name': admission.class_name.name if admission.class_name else '',
            'department': admission.department.name if admission.department else '',
            'updated_at': admission.updated_at.strftime('%d %b %Y'),
            'file_url': admission.file.url,
            'download_url': reverse('download_admission', kwargs={'pk': admission.id}),
        })

    return JsonResponse({'admissions': admissions_data})

def download_admission(request, pk):
    try:
        admission = Admission.objects.get(pk=pk)
        file_path = admission.file.path
        if not os.path.exists(file_path):
            return HttpResponseNotFound('The requested file was not found.')

        response = FileResponse(open(file_path, 'rb'), as_attachment=True, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{quote(os.path.basename(admission.file.name))}"'
        return response
    except Admission.DoesNotExist:
        return HttpResponseNotFound('Admission not found.')
    except Exception as e:
        print(f"Error downloading admission: {e}")
        return HttpResponseServerError('An error occurred during download.')

def view_admission_pdf(request, pk):
    try:
        admission = Admission.objects.get(pk=pk)
        response = FileResponse(admission.file.open(), content_type='application/pdf')
        return response
    except Admission.DoesNotExist:
        return HttpResponseNotFound('Admission not found.')
    except Exception as e:
        print(f"Error viewing admission PDF: {e}")
        return HttpResponseServerError('An error occurred while viewing the PDF.')

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
        # Ensure we have a valid YouTube ID
        if not video.youtube_id and video.youtube_url:
            video.youtube_id = video.extract_youtube_id(video.youtube_url)
            video.save()
        
        if video.youtube_id:  # Only include videos with valid YouTube IDs
            videos_data.append({
                'id': video.id,
                'title': video.title,
                'youtube_id': video.youtube_id,
                'description': video.description,
                'embed_url': video.embed_url,
                'thumbnail_url': video.thumbnail_url,
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




# --- NEW DEDICATED FOOTER VIEW ---
def footer_view(request):
    """
    This view fetches all the data needed for the footer component.
    """
    # The school_info object is already available everywhere via context processor,
    # but fetching it here ensures the footer can be loaded independently if needed.
    school_info = SchoolInfo.objects.first()
    important_links = ImportantLink.objects.filter(is_active=True).order_by('order')[:5]

    context = {
        'school_info': school_info,
        'footer_links': important_links,
    }
    return render(request, 'website/include/footer.html', context)


# --- RECENT EVENTS VIEW ---
def recent_events(request):
    """
    This view displays all recent events and news in a responsive grid layout.
    """
    events = EventAndNews.objects.filter(status=True).order_by('-created_at')
    
    context = {
        'events': events,
        'total_events': events.filter(type='EVENT').count(),
        'total_news': events.filter(type='NEWS').count(),
    }
    
    return render(request, 'website/recent_events.html', context)


# --- RECENT EVENTS VIEW (Alternative implementation) ---
def recent_events_view(request):
    """
    Fetches EventAndNews objects where status=True
    Orders them by created_at DESC
    Passes to template as context['events']
    Renders in recent_events.html
    """
    events = EventAndNews.objects.filter(status=True).order_by('-created_at')
    
    context = {
        'events': events,
    }
    
    return render(request, 'recent_events.html', context)



