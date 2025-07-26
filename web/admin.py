from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import *

# Resource classes for import/export
class StudentResource(resources.ModelResource):
    class_name = fields.Field(
        column_name='class_name',
        attribute='class_name',
        widget=ForeignKeyWidget(Class, 'name_en')
    )
    department = fields.Field(
        column_name='department',
        attribute='department',
        widget=ForeignKeyWidget(Department, 'name_en')
    )
    
    class Meta:
        model = Student
        import_id_fields = ('registration_number',)
        fields = ('name', 'roll_number', 'registration_number', 'class_name', 
                 'department', 'guardian_name', 'guardian_phone', 'address')

class TeacherResource(resources.ModelResource):
    class Meta:
        model = Teacher
        fields = ('name', 'position', 'education', 'specialization', 'experience',
                 'facebook', 'twitter', 'linkedin', 'email', 'phone', 'is_special_officer')

class NoticeResource(resources.ModelResource):
    class Meta:
        model = Notice
        fields = ('title', 'type', 'date', 'is_active')

# Admin classes
@admin.register(SchoolInfo)
class SchoolInfoAdmin(ImportExportModelAdmin):
    list_display = ('name', 'email', 'phone', 'established_year')
    search_fields = ('name', 'email', 'phone')

@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('name', 'name_en', 'icon', 'slug')
    search_fields = ('name', 'name_en')
    prepopulated_fields = {'slug': ('name_en',)}

@admin.register(Class)
class ClassAdmin(ImportExportModelAdmin):
    list_display = ('name', 'name_en', 'numeric_value')
    search_fields = ('name', 'name_en')
    ordering = ('numeric_value',)

@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    resource_class = TeacherResource
    list_display = ('name', 'position', 'email', 'phone', 'is_special_officer')
    list_filter = ('is_special_officer', 'position')
    search_fields = ('name', 'position', 'email', 'phone')

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    list_display = ('name', 'roll_number', 'registration_number', 'class_name', 'department')
    list_filter = ('class_name', 'department')
    search_fields = ('name', 'roll_number', 'registration_number', 'guardian_name')

@admin.register(Notice)
class NoticeAdmin(ImportExportModelAdmin):
    resource_class = NoticeResource
    list_display = ('title', 'type', 'date', 'is_active')
    list_filter = ('type', 'is_active', 'date')
    search_fields = ('title',)
    ordering = ('-date',)

@admin.register(Gallery)
class GalleryAdmin(ImportExportModelAdmin):
    list_display = ('title', 'category', 'is_slider')
    list_filter = ('category', 'is_slider')
    search_fields = ('title', 'description')

@admin.register(PrincipalRole)
class PrincipalRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_editable = ('is_active', 'order')
    ordering = ('order', '-created_at')

@admin.register(PrincipalMessage)
class PrincipalMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_active', 'order')
    list_filter = ('role', 'is_active')
    search_fields = ('name', 'message', 'role__name')
    list_editable = ('is_active', 'order')
    ordering = ('order', '-created_at')

@admin.register(ImportantLink)
class ImportantLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'icon', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title', 'url', 'icon')
    list_editable = ('is_active', 'order')
    ordering = ('order', '-created_at')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    list_editable = ('is_active', 'order')
    ordering = ('order', '-created_at')


@admin.register(NewsLink)
class NewsLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)
    list_editable = ('is_active',)


@admin.register(RoutineType)
class RoutineTypeAdmin(ImportExportModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Routine)
class RoutineAdmin(ImportExportModelAdmin):
    list_display = ('title', 'category', 'class_name', 'department', 'is_active', 'updated_at')
    list_filter = ('category', 'is_active', 'class_name', 'department')
    search_fields = ('title',)
    ordering = ('-updated_at',)


@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    list_display = ('title', 'class_name', 'department', 'is_active', 'updated_at')
    list_filter = ('is_active', 'class_name', 'department')
    search_fields = ('title',)
    ordering = ('-updated_at',)


class ResultResource(resources.ModelResource):
    class_name = fields.Field(
        column_name='class_name',
        attribute='class_name',
        widget=ForeignKeyWidget(Class, 'name_en')
    )
    department = fields.Field(
        column_name='department',
        attribute='department',
        widget=ForeignKeyWidget(Department, 'name_en')
    )

    class Meta:
        model = Result
        fields = ('title', 'class_name', 'department', 'is_active')

@admin.register(Result)
class ResultAdmin(ImportExportModelAdmin):
    resource_class = ResultResource
    list_display = ('title', 'class_name', 'department', 'is_active', 'created_at')
    list_filter = ('class_name', 'department', 'is_active')
    search_fields = ('title',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


class VideoResource(resources.ModelResource):
    class Meta:
        model = Video
        fields = ('title', 'youtube_id', 'description', 'is_active')

@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    resource_class = VideoResource
    list_display = ('title', 'youtube_id', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'youtube_id', 'description')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


class InformationSliderResource(resources.ModelResource):
    class Meta:
        model = InformationSlider
        fields = ('title', 'description', 'order', 'is_active')

class FacilityInfoResource(resources.ModelResource):
    class Meta:
        model = FacilityInfo
        fields = ('facility_type', 'title', 'description', 'icon', 'count', 'unit', 'order', 'is_active')


class FacultyInfoResource(resources.ModelResource):
    class Meta:
        model = FacultyInfo
        fields = ('name', 'position', 'department', 'education', 'experience', 'email', 'phone', 'order', 'is_active')


@admin.register(InformationService)
class InformationServiceAdmin(ImportExportModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('-created_at',)


@admin.register(InformationSlider)
class InformationSliderAdmin(ImportExportModelAdmin):
    resource_class = InformationSliderResource
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('order', '-created_at')
    list_editable = ('order', 'is_active')


@admin.register(FacilityInfo)
class FacilityInfoAdmin(ImportExportModelAdmin):
    resource_class = FacilityInfoResource
    list_display = ('facility_type', 'title', 'count', 'unit', 'order', 'is_active')
    list_filter = ('facility_type', 'is_active')
    search_fields = ('title', 'description')
    ordering = ('order', '-created_at')
    list_editable = ('order', 'is_active')


@admin.register(FacultyInfo)
class FacultyInfoAdmin(ImportExportModelAdmin):
    resource_class = FacultyInfoResource
    list_display = ('name', 'position', 'department', 'experience', 'email', 'order', 'is_active')
    list_filter = ('is_active', 'department')
    search_fields = ('name', 'position', 'department', 'email')
    ordering = ('order', '-created_at')
    list_editable = ('order', 'is_active')

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'address', 'phone', 'email')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'title', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'phone', 'title', 'message')
    list_editable = ('is_read',)




