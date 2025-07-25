from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class SchoolInfo(TimeStampModel):
    name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='school/')
    established_year = models.CharField(max_length=4)
    description = models.TextField()
    history = models.TextField()
    vision = models.TextField()
    mission = models.TextField()
    
    class Meta:
        verbose_name_plural = 'School Information'
    
    def __str__(self):
        return self.name

class Department(TimeStampModel):
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)  # English name
    icon = models.CharField(max_length=50)  # FontAwesome icon class
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Class(TimeStampModel):
    name = models.CharField(max_length=50)  # Bengali name
    name_en = models.CharField(max_length=50)  # English name
    numeric_value = models.IntegerField()  # For sorting (e.g., 6,7,8)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Classes'
        ordering = ['numeric_value']
    
    def __str__(self):
        return self.name

class Teacher(TimeStampModel):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='teachers/')
    education = models.CharField(max_length=200, blank=True)
    specialization = models.CharField(max_length=200, blank=True)
    experience = models.TextField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_special_officer = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.position}"

class Student(TimeStampModel):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20)
    registration_number = models.CharField(max_length=20)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to='students/', blank=True)
    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=20)
    address = models.TextField()
    
    def __str__(self):
        return f"{self.name} - {self.class_name} ({self.roll_number})"

class Notice(TimeStampModel):
    NOTICE_TYPES = (
        ('notice', 'Notice'),
        ('result', 'Result'),
        ('admission', 'Admission'),
        ('routine', 'Routine')
    )
    
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=NOTICE_TYPES)
    date = models.DateField()
    file = models.FileField(
        upload_to='notices/',
        validators=[FileExtensionValidator(['pdf'])]
    )
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.title}"

class Gallery(TimeStampModel):
    CATEGORIES = (
        ('school', 'School'),
        ('event', 'Event'),
        ('student', 'Student'),
        ('teacher', 'Teacher')
    )
    
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=20, choices=CATEGORIES)
    description = models.TextField(blank=True)
    is_slider = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Galleries'
    
    def __str__(self):
        return self.title

class PrincipalMessage(TimeStampModel):
    name = models.CharField(max_length=100)
    message = models.TextField()
    photo = models.ImageField(upload_to='principal/')
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if self.is_active:
            # Set all other messages to inactive
            PrincipalMessage.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Principal Message - {self.name}"




class RoutineType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Routine(models.Model):
    ROUTINE_CATEGORIES = (
        ('class', 'Class Routine'),
        ('exam', 'Exam Routine'),
    )
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=ROUTINE_CATEGORIES)
    routine_type = models.ForeignKey(RoutineType, on_delete=models.SET_NULL, null=True, blank=True)
    class_name = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='routines/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.get_category_display()} - {self.title}"



class Book(models.Model):
    title = models.CharField(max_length=200)
    class_name = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='books/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.title


class Result(TimeStampModel):
    title = models.CharField(max_length=255)
    file = models.FileField(
        upload_to='results/',
        validators=[FileExtensionValidator(['pdf'])]
    )
    class_name = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Results"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Video(TimeStampModel):
    title = models.CharField(max_length=255)
    youtube_id = models.CharField(max_length=50, help_text="The YouTube video ID (e.g., dQw4w9WgXcQ)")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Videos"
        ordering = ['-created_at']

    def __str__(self):
        return self.title