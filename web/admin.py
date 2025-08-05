# web/admin.py

from django.contrib import admin
from django.utils.html import format_html

# --- IMPORTS FOR UNFOLD AND IMPORT/EXPORT ---
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin

from .models import *

# --- COMBINED ADMIN CLASS FOR UNFOLD + IMPORT/EXPORT ---
# All your classes will inherit from this for a consistent look and functionality.
class CustomModelAdmin(ImportExportModelAdmin, ModelAdmin):
    pass

# --- Core School Structure ---

@admin.register(SchoolInfo)
class SchoolInfoAdmin(ModelAdmin):  # SchoolInfo is a singleton, no import/export needed
    list_display = ('name', 'reg_no', 'email', 'phone', 'established_year')
    fieldsets = (
        ('Basic Information', {'fields': ('name', 'reg_no', 'logo', 'favicon', 'established_year')}),
        ('Contact Details', {'fields': ('address', 'email', 'phone')}),
        ('Social Media Links', {'fields': ('facebook_url', 'instagram_url', 'youtube_url', 'linkedin_url')}),
        ('School Identity', {'fields': ('description', 'history', 'vision', 'mission')}),
    )
    def has_add_permission(self, request):
        return SchoolInfo.objects.count() == 0

@admin.register(Department)
class DepartmentAdmin(CustomModelAdmin):
    list_display = ('name', 'name_en', 'slug')
    search_fields = ('name', 'name_en')
    prepopulated_fields = {'slug': ('name_en',)}

@admin.register(Class)
class ClassAdmin(CustomModelAdmin):
    list_display = ('name', 'name_en', 'numeric_value')
    search_fields = ('name', 'name_en')
    ordering = ('numeric_value',)

@admin.register(Teacher)
class TeacherAdmin(CustomModelAdmin):
    list_display = ('name', 'position', 'category', 'email', 'phone', 'image_preview')
    list_filter = ('category', 'is_special_officer')
    search_fields = ('name', 'position', 'email', 'phone')
    fieldsets = (
        (None, {'fields': ('name', 'position', 'photo')}),
        ('Categorization', {'fields': ('category', 'is_special_officer')}),
        ('Qualifications', {'fields': ('education', 'specialization', 'experience')}),
        ('Contact', {'fields': ('email', 'phone')}),
        ('Social Media', {'classes': ('collapse',), 'fields': ('facebook', 'twitter', 'linkedin')}),
    )
    def image_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 5px;" />', obj.photo.url)
        return "No Image"
    image_preview.short_description = 'Photo'

@admin.register(FacultyMember)
class FacultyMemberAdmin(CustomModelAdmin):
    list_display = ('name', 'position', 'category', 'department', 'email', 'phone', 'is_active', 'order', 'image_preview')
    list_filter = ('category', 'is_active', 'department')
    search_fields = ('name', 'position', 'email', 'phone', 'department')
    list_editable = ('is_active', 'order')
    fieldsets = (
        ('Basic Information', {'fields': ('name', 'position', 'photo', 'category')}),
        ('Professional Details', {'fields': ('department', 'education', 'experience')}),
        ('Contact Information', {'fields': ('email', 'phone')}),
        ('Settings', {'fields': ('is_active', 'order')}),
    )
    def image_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 5px;" />', obj.photo.url)
        return "No Image"
    image_preview.short_description = 'Photo'

@admin.register(Student)
class StudentAdmin(CustomModelAdmin):
    list_display = ('name', 'roll_number', 'class_name', 'department', 'guardian_name', 'guardian_phone')
    search_fields = ('name', 'roll_number', 'registration_number', 'class_name__name', 'department__name')
    list_filter = ('class_name', 'department')
    autocomplete_fields = ('class_name', 'department')
    fieldsets = (
        ('Student Identity', {'fields': ('name', 'photo', 'roll_number', 'registration_number')}),
        ('Academic Details', {'fields': ('class_name', 'department')}),
        ('Guardian Information', {'fields': ('guardian_name', 'guardian_phone', 'address')}),
    )

# --- Content and File Management ---

@admin.register(Notice)
class NoticeAdmin(CustomModelAdmin):
    list_display = ('title', 'type', 'date', 'is_active')
    list_filter = ('type', 'is_active', 'date')
    search_fields = ('title',)
    list_editable = ('is_active',)

@admin.register(Slider)
class SliderAdmin(CustomModelAdmin):
    """
    Admin configuration for the Slider model.
    """
    list_display = ('image_thumbnail', 'title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)
    list_editable = ('is_active', 'title')
    ordering = ('-created_at',)
    
    readonly_fields = ('image_thumbnail',)

    def image_thumbnail(self, obj):
        """
        Creates an HTML image tag for the admin list/detail view.
        """
        if obj.image:
            return format_html('<img src="{}" style="max-width: 200px; max-height: 100px;" />', obj.image.url)
        return "No Image Uploaded"
    
    image_thumbnail.short_description = 'Image Preview'




@admin.register(Gallery)
class GalleryAdmin(CustomModelAdmin):
    list_display = ('title', 'category', 'is_slider', 'image_preview')
    list_filter = ('category', 'is_slider')
    search_fields = ('title', 'description')
    list_editable = ('is_slider',)
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border-radius: 5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

@admin.register(RoutineType)
class RoutineTypeAdmin(CustomModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Routine)
class RoutineAdmin(CustomModelAdmin):
    list_display = ('title', 'category', 'routine_type', 'class_name', 'department', 'is_active')
    list_filter = ('category', 'routine_type', 'class_name', 'department', 'is_active')
    search_fields = ('title',)
    autocomplete_fields = ('routine_type', 'class_name', 'department')
    list_editable = ('is_active',)

@admin.register(Book)
class BookAdmin(CustomModelAdmin):
    list_display = ('title', 'class_name', 'department', 'is_active')
    list_filter = ('class_name', 'department', 'is_active')
    search_fields = ('title',)
    autocomplete_fields = ('class_name', 'department')
    list_editable = ('is_active',)

@admin.register(Syllabus)
class SyllabusAdmin(CustomModelAdmin):
    list_display = ('title', 'class_name', 'department', 'is_active', 'updated_at')
    list_filter = ('class_name', 'department', 'is_active')
    search_fields = ('title',)
    autocomplete_fields = ('class_name', 'department')
    list_editable = ('is_active',)
    date_hierarchy = 'updated_at'

@admin.register(Result)
class ResultAdmin(CustomModelAdmin):
    list_display = ('title', 'class_name', 'department', 'is_active', 'created_at')
    list_filter = ('class_name', 'department', 'is_active')
    search_fields = ('title',)
    autocomplete_fields = ('class_name', 'department')
    list_editable = ('is_active',)

@admin.register(Admission)
class AdmissionAdmin(CustomModelAdmin):
    list_display = ('title', 'class_name', 'department', 'is_active', 'created_at')
    list_filter = ('class_name', 'department', 'is_active')
    search_fields = ('title',)
    autocomplete_fields = ('class_name', 'department')
    list_editable = ('is_active',)

@admin.register(Video)
class VideoAdmin(CustomModelAdmin):
    list_display = ('title', 'youtube_id', 'video_preview', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('youtube_id', 'video_preview')
    
    fieldsets = (
        ('Video Information', {
            'fields': ('title', 'description', 'is_active')
        }),
        ('YouTube Settings', {
            'fields': ('youtube_url', 'youtube_id', 'video_preview'),
            'description': 'Paste the full YouTube URL (e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ). The video ID will be extracted automatically.'
        }),
    )
    
    def video_preview(self, obj):
        """Display video preview in admin"""
        if obj.youtube_id:
            return format_html(
                '<div style="width: 200px; height: 112px;">'
                '<iframe width="200" height="112" src="https://www.youtube.com/embed/{}" '
                'frameborder="0" allowfullscreen></iframe></div>',
                obj.youtube_id
            )
        return "No video"
    video_preview.short_description = "Video Preview"

# --- Leadership and Messages ---

@admin.register(PrincipalRole)
class PrincipalRoleAdmin(CustomModelAdmin):
    list_display = ('name', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('name',)

@admin.register(PrincipalMessage)
class PrincipalMessageAdmin(CustomModelAdmin):
    list_display = ('name', 'role', 'is_active', 'show_on_home_page')
    list_filter = ('role', 'is_active', 'show_on_home_page')
    list_editable = ('is_active', 'show_on_home_page')
    search_fields = ('name', 'message')
    autocomplete_fields = ('role',)
    fieldsets = (
        ("Message Details", {"fields": ('name', 'role', 'message', 'photo')}),
        ("Display Options", {"fields": ('is_active', 'show_on_home_page', 'order')}),
    )

# --- Site Configuration & Links ---

@admin.register(ImportantLink)
class ImportantLinkAdmin(CustomModelAdmin):
    list_display = ('title', 'url', 'icon', 'is_active', 'order')
    list_editable = ('is_active', 'order')

@admin.register(News)
class NewsAdmin(CustomModelAdmin):
    list_display = ('title', 'link', 'is_active', 'order')
    list_editable = ('is_active', 'order')

@admin.register(NewsLink)
class NewsLinkAdmin(CustomModelAdmin):
    list_display = ('title', 'is_active')

# --- Contact Management ---

@admin.register(ContactInfo)
class ContactInfoAdmin(ModelAdmin): # Singleton, no import/export
    list_display = ('title', 'phone', 'email', 'is_active')
    def has_add_permission(self, request):
        return ContactInfo.objects.count() == 0

@admin.register(ContactMessage)
class ContactMessageAdmin(CustomModelAdmin):
    list_display = ('title', 'name', 'phone', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('name', 'phone', 'title', 'message')
    readonly_fields = ('name', 'phone', 'title', 'message', 'created_at')
    list_display_links = ('title',)

# --- About Page Content Management ---

class AimPointInline(admin.TabularInline):
    model = AimPoint
    extra = 1

@admin.register(SchoolAims)
class SchoolAimsAdmin(CustomModelAdmin):
    list_display = ('title', 'is_active', 'order')
    inlines = [AimPointInline]

@admin.register(AboutPage)
class AboutPageAdmin(CustomModelAdmin):
    list_display = ('title', 'is_active')

@admin.register(SchoolHistory)
class SchoolHistoryAdmin(CustomModelAdmin):
    list_display = ('title', 'is_active', 'order')

@admin.register(SchoolBriefInfo)
class SchoolBriefInfoAdmin(CustomModelAdmin):
    list_display = ('title', 'teachers_count', 'students_count', 'is_active')

@admin.register(AboutMessage)
class AboutMessageAdmin(CustomModelAdmin):
    list_display = ('title', 'name', 'position', 'serial_no', 'show_on_home_page', 'is_active')
    list_filter = ('is_active', 'show_on_home_page')
    ordering = ('serial_no',)
    readonly_fields = ('show_on_home_page',)  # Make it readonly since it's auto-set based on serial_no

@admin.register(SchoolApproval)
class SchoolApprovalAdmin(CustomModelAdmin):
    list_display = ('title', 'is_active', 'order')

@admin.register(SchoolRecognition)
class SchoolRecognitionAdmin(CustomModelAdmin):
    list_display = ('title', 'is_active', 'order')

@admin.register(EventNewsImage)
class EventNewsImageAdmin(CustomModelAdmin):
    list_display = ('title', 'image_preview', 'uploaded_at')
    search_fields = ('title',)
    readonly_fields = ('uploaded_at',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

@admin.register(EventAndNews)
class EventAndNewsAdmin(CustomModelAdmin):
    list_display = ('title', 'type', 'status', 'created_at', 'primary_image_preview')
    list_filter = ('type', 'status', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('status',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'type', 'status')
        }),
        ('Content', {
            'fields': ('description', 'primary_image')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    
    def primary_image_preview(self, obj):
        if obj.primary_image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 5px;" />', obj.primary_image.url)
        return "No Image"
    primary_image_preview.short_description = 'Primary Image'


class EventAndNewsImageInline(admin.TabularInline):
    model = EventAndNewsImage
    extra = 1
    fields = ('image', 'title', 'description', 'order', 'image_preview')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'


# Update the EventAndNewsAdmin to include the inline
EventAndNewsAdmin.inlines = [EventAndNewsImageInline]


@admin.register(AboutLink)
class AboutLinkAdmin(CustomModelAdmin):
    list_display = ('title', 'url', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('title',)
    
# --- Information Service & Facilities (Optional Sections) ---

@admin.register(InformationService)
class InformationServiceAdmin(CustomModelAdmin):
    list_display = ('title', 'is_active')

@admin.register(InformationSlider)
class InformationSliderAdmin(CustomModelAdmin):
    list_display = ('title', 'order', 'is_active', 'image_preview')
    list_editable = ('order', 'is_active')
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border-radius: 5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

@admin.register(FacilityInfo)
class FacilityInfoAdmin(CustomModelAdmin):
    list_display = ('title', 'facility_type', 'count', 'unit', 'order', 'is_active')
    list_filter = ('facility_type',)
    list_editable = ('order', 'is_active')

@admin.register(FacultyInfo)
class FacultyInfoAdmin(CustomModelAdmin):
    list_display = ('name', 'position', 'department', 'order', 'is_active', 'image_preview')
    list_filter = ('department',)
    search_fields = ('name', 'position')
    list_editable = ('order', 'is_active')
    def image_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 5px;" />', obj.photo.url)
        return "No Image"
    image_preview.short_description = 'Photo'