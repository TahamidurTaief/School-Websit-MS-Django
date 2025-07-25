from django.contrib import admin
from .models import Notice, NoticeType

@admin.register(NoticeType)
class NoticeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'notice_type', 'class_name', 'department', 'is_active', 'created_at')
    list_filter = ('notice_type', 'class_name', 'department', 'is_active')
    search_fields = ('title', 'short_description')
    raw_id_fields = ('class_name', 'department', 'notice_type')
    date_hierarchy = 'created_at'