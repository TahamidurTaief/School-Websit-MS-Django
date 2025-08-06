from django.core.management.base import BaseCommand
from django.db import connection
from web.models import Student, Class, Department

class Command(BaseCommand):
    help = 'Check database integrity for foreign key constraints'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Checking database integrity...'))
        
        # Check for orphaned students without valid class
        orphaned_students = Student.objects.filter(class_name__isnull=True)
        if orphaned_students.exists():
            self.stdout.write(
                self.style.WARNING(
                    f'Found {orphaned_students.count()} students without valid class'
                )
            )
        
        # Check for students with invalid class references
        try:
            invalid_class_refs = []
            for student in Student.objects.all():
                try:
                    # This will raise an exception if the class doesn't exist
                    _ = student.class_name.name
                except:
                    invalid_class_refs.append(student)
            
            if invalid_class_refs:
                self.stdout.write(
                    self.style.WARNING(
                        f'Found {len(invalid_class_refs)} students with invalid class references'
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error checking class references: {str(e)}')
            )
        
        # Check for students with invalid department references
        try:
            invalid_dept_refs = []
            for student in Student.objects.exclude(department__isnull=True):
                try:
                    # This will raise an exception if the department doesn't exist
                    _ = student.department.name
                except:
                    invalid_dept_refs.append(student)
            
            if invalid_dept_refs:
                self.stdout.write(
                    self.style.WARNING(
                        f'Found {len(invalid_dept_refs)} students with invalid department references'
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error checking department references: {str(e)}')
            )
        
        # Check foreign key constraints at database level
        try:
            with connection.cursor() as cursor:
                cursor.execute("PRAGMA foreign_key_check;")
                constraint_violations = cursor.fetchall()
                
                if constraint_violations:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Found {len(constraint_violations)} foreign key constraint violations:'
                        )
                    )
                    for violation in constraint_violations:
                        self.stdout.write(self.style.ERROR(f'  {violation}'))
                else:
                    self.stdout.write(
                        self.style.SUCCESS('No foreign key constraint violations found.')
                    )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error checking foreign key constraints: {str(e)}')
            )
        
        self.stdout.write(self.style.SUCCESS('Integrity check completed.'))
