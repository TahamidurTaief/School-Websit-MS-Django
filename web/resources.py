from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Class, Student, Department

class ClassResource(resources.ModelResource):
    class Meta:
        model = Class
        fields = ('id', 'name', 'name_en', 'numeric_value', 'description')
        export_order = ('id', 'name', 'name_en', 'numeric_value', 'description')
        
    def before_save_instance(self, instance, using_transactions, dry_run):
        # Validate numeric_value uniqueness
        if Class.objects.filter(numeric_value=instance.numeric_value).exclude(pk=instance.pk).exists():
            raise ValueError(f"Class with numeric_value {instance.numeric_value} already exists")
    
    def after_delete_instance(self, instance, using_transactions, dry_run):
        # Log when a class is deleted (which will cascade delete students)
        if not dry_run:
            student_count = instance.student_set.count()
            if student_count > 0:
                print(f"Deleted class '{instance.name}' and {student_count} associated students")

class StudentResource(resources.ModelResource):
    class_name = fields.Field(
        column_name='class_name',
        attribute='class_name',
        widget=ForeignKeyWidget(Class, 'name')
    )
    department = fields.Field(
        column_name='department',
        attribute='department',
        widget=ForeignKeyWidget(Department, 'name')
    )
    
    class Meta:
        model = Student
        fields = ('id', 'name', 'roll_number', 'registration_number', 'class_name', 'department', 'guardian_name', 'guardian_phone', 'address')
        export_order = ('id', 'name', 'roll_number', 'registration_number', 'class_name', 'department', 'guardian_name', 'guardian_phone', 'address')
    
    def before_save_instance(self, instance, using_transactions, dry_run):
        # Ensure class_name is not None
        if not instance.class_name:
            raise ValueError("Student must have a valid class assigned")
        
        # Validate roll_number uniqueness within the class
        if Student.objects.filter(
            roll_number=instance.roll_number, 
            class_name=instance.class_name
        ).exclude(pk=instance.pk).exists():
            raise ValueError(f"Student with roll number {instance.roll_number} already exists in class {instance.class_name}")
