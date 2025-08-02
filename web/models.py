from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class SchoolInfo(TimeStampModel):
    name = models.CharField(max_length=255, verbose_name="School Name")
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='school/', help_text="Upload the main logo for the navbar.")
    favicon = models.ImageField(upload_to='school/', blank=True, null=True, help_text="Upload a .ico or .png file for the browser tab icon.")
    established_year = models.CharField(max_length=4)
    description = models.TextField()
    history = models.TextField()
    vision = models.TextField()
    mission = models.TextField()
    reg_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Registration Number")
    # New Social Link Fields
    facebook_url = models.URLField(max_length=255, blank=True, null=True, verbose_name="Facebook URL")
    instagram_url = models.URLField(max_length=255, blank=True, null=True, verbose_name="Instagram URL")
    youtube_url = models.URLField(max_length=255, blank=True, null=True, verbose_name="YouTube URL")
    linkedin_url = models.URLField(max_length=255, blank=True, null=True, verbose_name="LinkedIn URL")

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
    CATEGORY_CHOICES = [
        ('special_officer', 'Special Officer'),
        ('teacher', 'Teacher'),
        ('management_board', 'Management Board'),
    ]
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, default='teacher', verbose_name='Category')
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


class Slider(models.Model):
    image = models.ImageField(upload_to='sliders/')
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Sliders'
        ordering = ['-created_at']
    def __str__(self):
        return self.title if self.title else f"Slider {self.id}"

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

        

class PrincipalRole(TimeStampModel):
    name = models.CharField(max_length=100, verbose_name='Role Name')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Principal/Head Role'
        verbose_name_plural = 'Principal/Head Roles'

    def __str__(self):
        return self.name
    


class PrincipalMessage(TimeStampModel):
    name = models.CharField(max_length=100)
    role = models.ForeignKey(PrincipalRole, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Role')
    message = models.TextField()
    photo = models.ImageField(upload_to='principal/', blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    show_on_home_page = models.BooleanField(
        default=False,
        verbose_name="Show on home page",
        help_text="Check this box to feature this message on the home page. Only one can be selected."
    )

    def save(self, *args, **kwargs):
        # If this message is being set to show on the home page
        if self.show_on_home_page:
            # Unset any other message that might be currently featured
            PrincipalMessage.objects.filter(show_on_home_page=True).exclude(pk=self.pk).update(show_on_home_page=False)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Principal/Head Message'
        verbose_name_plural = 'Principal/Head Messages'

    def __str__(self):
        return f"{self.role} - {self.name}" if self.role else self.name
    



class ImportantLink(TimeStampModel):
    title = models.CharField(max_length=200, verbose_name='শিরোনাম')
    url = models.URLField(verbose_name='লিঙ্ক')
    icon = models.CharField(max_length=50, blank=True, verbose_name='আইকন (FontAwesome)')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'গুরুত্বপূর্ণ লিঙ্ক'
        verbose_name_plural = 'গুরুত্বপূর্ণ লিঙ্কসমূহ'

    def __str__(self):
        return self.title

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

class InformationService(TimeStampModel):
    """Main model for Information Service Center"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Information Service"

    def __str__(self):
        return self.title

class InformationSlider(TimeStampModel):
    """Sliding photo gallery for information service"""
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='information_slider/')
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = "Information Sliders"

    def __str__(self):
        return self.title

class FacilityInfo(TimeStampModel):
    """School facilities information"""
    FACILITY_TYPES = (
        ('classroom', 'কক্ষ সংখ্যা'),
        ('computer', 'কম্পিউটার ব্যবহার'),
        ('seats', 'ছাত্রছাত্রীর আসন সংখ্যা'),
        ('multimedia', 'মাল্টিমিডিয়া ক্লাসরুম'),
        ('transport', 'যানবাহন সুবিধা'),
    )

    facility_type = models.CharField(max_length=20, choices=FACILITY_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class")
    count = models.IntegerField(default=0, help_text="Number/Count for this facility")
    unit = models.CharField(max_length=20, blank=True, help_text="Unit (e.g., 'টি', 'জন', 'খানা')")
    image = models.ImageField(upload_to='facilities/', blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = "Facility Information"

    def __str__(self):
        return f"{self.get_facility_type_display()} - {self.title}"

class FacultyInfo(TimeStampModel):
    """Faculty information for information service"""
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    department = models.CharField(max_length=200, blank=True)
    education = models.CharField(max_length=200, blank=True)
    experience = models.CharField(max_length=100, blank=True, help_text="Years of experience")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='faculty/', blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = "Faculty Information"

    def __str__(self):
        return f"{self.name} - {self.position}"

class ContactInfo(TimeStampModel):
    """Public contact information for the school"""
    title = models.CharField(max_length=200, verbose_name='শিরোনাম')
    address = models.TextField(verbose_name='ঠিকানা')
    phone = models.CharField(max_length=30, verbose_name='ফোন নম্বর')
    email = models.EmailField(verbose_name='ইমেইল')
    map_embed = models.TextField(blank=True, verbose_name='গুগল ম্যাপ এম্বেড কোড', help_text='গুগল ম্যাপ এম্বেড কোড (ঐচ্ছিক)')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')

    class Meta:
        verbose_name = 'যোগাযোগের তথ্য'
        verbose_name_plural = 'যোগাযোগের তথ্যসমূহ'

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    """Messages submitted via the public contact form"""
    name = models.CharField(max_length=100, verbose_name='নাম')
    phone = models.CharField(max_length=30, verbose_name='ফোন নম্বর')
    title = models.CharField(max_length=200, verbose_name='বার্তার শিরোনাম')
    message = models.TextField(verbose_name='বার্তার বিবরণ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='পাঠানোর সময়')
    is_read = models.BooleanField(default=False, verbose_name='পড়া হয়েছে')

    class Meta:
        verbose_name = 'যোগাযোগ বার্তা'
        verbose_name_plural = 'যোগাযোগ বার্তাসমূহ'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.name} ({self.phone})"

class News(TimeStampModel):
    """News items for the home page"""
    title = models.CharField(max_length=200, verbose_name='শিরোনাম')
    description = models.TextField(blank=True, verbose_name='বিবরণ')
    link = models.URLField(verbose_name='লিঙ্ক')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.IntegerField(default=0, verbose_name='ক্রম')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'সংবাদ'
        verbose_name_plural = 'সংবাদসমূহ'

    def __str__(self):
        return self.title

class NewsLink(TimeStampModel):
    """News and Links section for home page"""
    title = models.CharField(max_length=200, verbose_name='শিরোনাম', default='সংবাদ/প্রয়োজনীয় লিংক')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')

    class Meta:
        verbose_name = 'সংবাদ ও লিঙ্ক বিভাগ'
        verbose_name_plural = 'সংবাদ ও লিঙ্ক বিভাগসমূহ'

    def __str__(self):
        return self.title

# About Page Models
class AboutPage(TimeStampModel):
    """Main about page configuration"""
    title = models.CharField(max_length=200, default='আমাদের সম্পর্কে (About Us)', verbose_name='পৃষ্ঠার শিরোনাম')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')

    class Meta:
        verbose_name = 'আমাদের সম্পর্কে পৃষ্ঠা'
        verbose_name_plural = 'আমাদের সম্পর্কে পৃষ্ঠা'

    def __str__(self):
        return self.title

class SchoolHistory(TimeStampModel):
    """School history section"""
    title = models.CharField(max_length=200, default='প্রতিষ্ঠানের ইতিহাস', verbose_name='শিরোনাম')
    content = models.TextField(verbose_name='বিস্তারিত বিবরণ')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.IntegerField(default=0, verbose_name='ক্রম')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'প্রতিষ্ঠানের ইতিহাস'
        verbose_name_plural = 'প্রতিষ্ঠানের ইতিহাস'

    def __str__(self):
        return self.title

class SchoolBriefInfo(TimeStampModel):
    """School brief information with statistics"""
    title = models.CharField(max_length=200, default='সংক্ষিপ্ত তথ্য', verbose_name='শিরোনাম')
    description = models.TextField(verbose_name='বিস্তারিত বিবরণ')
    teachers_count = models.CharField(max_length=20, default='৫০+', verbose_name='শিক্ষক-শিক্ষিকার সংখ্যা')
    departments_count = models.CharField(max_length=20, default='৫', verbose_name='বিভাগের সংখ্যা')
    classrooms_count = models.CharField(max_length=20, default='৩০+', verbose_name='ক্লাসরুমের সংখ্যা')
    students_count = models.CharField(max_length=20, default='১০০০+', verbose_name='শিক্ষার্থীর সংখ্যা')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.IntegerField(default=0, verbose_name='ক্রম')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'সংক্ষিপ্ত তথ্য'
        verbose_name_plural = 'সংক্ষিপ্ত তথ্য'

    def __str__(self):
        return self.title

class AboutPrincipalMessage(TimeStampModel):
    """Principal message for about page"""
    title = models.CharField(max_length=200, default='অধ্যক্ষের বাণী', verbose_name='শিরোনাম')
    name = models.CharField(max_length=100, verbose_name='নাম')
    message = models.TextField(verbose_name='বার্তা')
    photo = models.ImageField(upload_to='about/principal/', blank=True, verbose_name='ছবি')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.IntegerField(default=0, verbose_name='ক্রম')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'অধ্যক্ষের বাণী (আমাদের সম্পর্কে)'
        verbose_name_plural = 'অধ্যক্ষের বাণী (আমাদের সম্পর্কে)'

    def __str__(self):
        return f"{self.title} - {self.name}"

class SchoolApproval(TimeStampModel):
    """School approval and recognition information"""
    title = models.CharField(max_length=200, default='অনুমোদন', verbose_name='শিরোনাম')
    content = models.TextField(verbose_name='বিস্তারিত বিবরণ')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.IntegerField(default=0, verbose_name='ক্রম')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'অনুমোদন'
        verbose_name_plural = 'অনুমোদন'

    def __str__(self):
        return self.title

class SchoolBranch(TimeStampModel):
    """School branches information"""
    name = models.CharField(max_length=200, verbose_name='শাখার নাম')
    location = models.CharField(max_length=200, verbose_name='ঠিকানা')
    established_year = models.CharField(max_length=20, verbose_name='প্রতিষ্ঠাকাল')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.IntegerField(default=0, verbose_name='ক্রম')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'শাখা'
        verbose_name_plural = 'শাখাসমূহ'

    def __str__(self):
        return f"{self.name} - {self.location}"

class SchoolRecognition(TimeStampModel):
    """School recognition and awards"""
    title = models.CharField(max_length=200, default='স্বীকৃতি', verbose_name='শিরোনাম')
    content = models.TextField(verbose_name='বিস্তারিত বিবরণ')
    document = models.FileField(
        upload_to='recognition_documents/',
        blank=True,
        null=True,
        verbose_name='স্বীকৃতি দলিল',
        help_text='PDF, DOC, or image file'
    )
    document_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='দলিলের শিরোনাম',
        help_text='Document title to display'
    )
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.IntegerField(default=0, verbose_name='ক্রম')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'স্বীকৃতি'
        verbose_name_plural = 'স্বীকৃতি'

    def __str__(self):
        return self.title

class SchoolAims(TimeStampModel):
    """School aims and objectives"""
    title = models.CharField(max_length=200, default='লক্ষ্য ও উদ্দেশ্য', verbose_name='শিরোনাম')
    content = models.TextField(verbose_name='বিস্তারিত বিবরণ')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.IntegerField(default=0, verbose_name='ক্রম')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'লক্ষ্য ও উদ্দেশ্য'
        verbose_name_plural = 'লক্ষ্য ও উদ্দেশ্য'

    def __str__(self):
        return self.title

class AimPoint(TimeStampModel):
    """Individual aim points"""
    aim = models.ForeignKey(SchoolAims, on_delete=models.CASCADE, related_name='points', verbose_name='লক্ষ্য')
    point = models.CharField(max_length=500, verbose_name='লক্ষ্য পয়েন্ট')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.IntegerField(default=0, verbose_name='ক্রম')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'লক্ষ্য পয়েন্ট'
        verbose_name_plural = 'লক্ষ্য পয়েন্টসমূহ'

    def __str__(self):
        return self.point

class AboutNewsItem(TimeStampModel):
    """News items for about page"""
    title = models.CharField(max_length=200, verbose_name='সংবাদের শিরোনাম')
    date = models.CharField(max_length=50, verbose_name='তারিখ')
    link = models.URLField(verbose_name='লিঙ্ক')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.IntegerField(default=0, verbose_name='ক্রম')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'সংবাদ আইটেম'
        verbose_name_plural = 'সংবাদ আইটেমসমূহ'

    def __str__(self):
        return self.title

class AboutLink(TimeStampModel):
    """Important links for about page"""
    title = models.CharField(max_length=200, verbose_name='লিঙ্কের শিরোনাম')
    url = models.URLField(verbose_name='লিঙ্ক')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.IntegerField(default=0, verbose_name='ক্রম')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'গুরুত্বপূর্ণ লিঙ্ক'
        verbose_name_plural = 'গুরুত্বপূর্ণ লিঙ্কসমূহ'

    def __str__(self):
        return self.title