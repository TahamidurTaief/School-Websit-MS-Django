# web/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SchoolInfo, Department, Class, Teacher, Student, Notice, Gallery,
    PrincipalRole, PrincipalMessage, ImportantLink, RoutineType, Routine,
    Book, Result, Video, InformationService, InformationSlider, FacilityInfo,
    FacultyInfo, ContactInfo, ContactMessage, News, NewsLink, AboutPage,
    SchoolHistory, SchoolBriefInfo, AboutPrincipalMessage, SchoolApproval,
    SchoolBranch, SchoolRecognition, SchoolAims, AimPoint, AboutNewsItem, AboutLink
)

# A simple decorator to add a default description for admin sections
def section(title):
    def decorator(cls):
        cls.verbose_name_plural = title
        return cls
    return decorator

# --- Core School Structure ---

@admin.register(SchoolInfo)
class SchoolInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'established_year')
    
    fieldsets = (
        ('Basic Information', {'fields': ('name', 'logo', 'favicon', 'established_year')}),
        ('Contact Details', {'fields': ('address', 'email', 'phone')}),
        ('Social Media Links', {'fields': ('facebook_url', 'instagram_url', 'youtube_url', 'linkedin_url')}),
        ('School Identity', {'fields': ('description', 'history', 'vision', 'mission')}),
    )
    
    def has_add_permission(self, request):
        # Allow only one SchoolInfo object to be created
        return SchoolInfo.objects.count() == 0

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'slug')
    search_fields = ('name', 'name_en')
    prepopulated_fields = {'slug': ('name_en',)}

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'numeric_value')
    search_fields = ('name', 'name_en')
    ordering = ('numeric_value',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
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


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
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
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'date', 'is_active')
    list_filter = ('type', 'is_active', 'date')
    search_fields = ('title',)
    list_editable = ('is_active',)

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
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
class RoutineTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'routine_type', 'class_name', 'department', 'is_active')
    list_filter = ('category', 'routine_type', 'class_name', 'department', 'is_active')
    search_fields = ('title',)
    autocomplete_fields = ('routine_type', 'class_name', 'department')
    list_editable = ('is_active',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'class_name', 'department', 'is_active')
    list_filter = ('class_name', 'department', 'is_active')
    search_fields = ('title',)
    autocomplete_fields = ('class_name', 'department')
    list_editable = ('is_active',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('title', 'class_name', 'department', 'is_active', 'created_at')
    list_filter = ('class_name', 'department', 'is_active')
    search_fields = ('title',)
    autocomplete_fields = ('class_name', 'department')
    list_editable = ('is_active',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_id', 'is_active')
    search_fields = ('title',)
    list_editable = ('is_active',)


# --- Leadership and Messages ---

@admin.register(PrincipalRole)
class PrincipalRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('name',) # <-- THE FIX IS HERE

@admin.register(PrincipalMessage)
class PrincipalMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_active', 'show_on_home_page')
    list_filter = ('role', 'is_active', 'show_on_home_page')
    list_editable = ('is_active', 'show_on_home_page')
    search_fields = ('name', 'message')
    autocomplete_fields = ('role',)
    fieldsets = (
        ("Message Details", {
            "fields": ('name', 'role', 'message', 'photo')
        }),
        ("Display Options", {
            "fields": ('is_active', 'show_on_home_page', 'order')
        }),
    )

# --- Site Configuration & Links ---

@admin.register(ImportantLink)
class ImportantLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'icon', 'is_active', 'order')
    list_editable = ('is_active', 'order')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'is_active', 'order')
    list_editable = ('is_active', 'order')

@admin.register(NewsLink)
class NewsLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')

# --- Contact Management ---

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'email', 'is_active')
    
    def has_add_permission(self, request):
        return ContactInfo.objects.count() == 0

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
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
class SchoolAimsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    inlines = [AimPointInline]

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')

@admin.register(SchoolHistory)
class SchoolHistoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')

@admin.register(SchoolBriefInfo)
class SchoolBriefInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'teachers_count', 'students_count', 'is_active')

@admin.register(AboutPrincipalMessage)
class AboutPrincipalMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'is_active', 'order')

@admin.register(SchoolApproval)
class SchoolApprovalAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')

@admin.register(SchoolBranch)
class SchoolBranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'established_year', 'is_active')

@admin.register(SchoolRecognition)
class SchoolRecognitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    
@admin.register(AboutNewsItem)
class AboutNewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'link', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('title',)

@admin.register(AboutLink)
class AboutLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('title',)
    
# --- Information Service & Facilities (Optional Sections) ---

@admin.register(InformationService)
class InformationServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')

@admin.register(InformationSlider)
class InformationSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'image_preview')
    list_editable = ('order', 'is_active')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border-radius: 5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'


@admin.register(FacilityInfo)
class FacilityInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'facility_type', 'count', 'unit', 'order', 'is_active')
    list_filter = ('facility_type',)
    list_editable = ('order', 'is_active')

@admin.register(FacultyInfo)
class FacultyInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'department', 'order', 'is_active', 'image_preview')
    list_filter = ('department',)
    search_fields = ('name', 'position')
    list_editable = ('order', 'is_active')

    def image_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 5px;" />', obj.photo.url)
        return "No Image"
    image_preview.short_description = 'Photo'