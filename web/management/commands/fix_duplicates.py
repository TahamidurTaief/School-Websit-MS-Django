from django.core.management.base import BaseCommand
from django.db.models import Count
from web.models import Student, Class

class Command(BaseCommand):
    help = 'Find and fix duplicate student roll numbers within classes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Actually fix the duplicates by adding suffixes',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Checking for duplicate roll numbers...'))
        
        # Find students with duplicate roll numbers in the same class
        duplicates = (Student.objects
                     .values('roll_number', 'class_name')
                     .annotate(count=Count('id'))
                     .filter(count__gt=1))
        
        if not duplicates:
            self.stdout.write(self.style.SUCCESS('No duplicate roll numbers found.'))
            return
        
        self.stdout.write(
            self.style.WARNING(f'Found {len(duplicates)} sets of duplicate roll numbers.')
        )
        
        for duplicate in duplicates:
            roll_number = duplicate['roll_number']
            class_id = duplicate['class_name']
            count = duplicate['count']
            
            try:
                class_obj = Class.objects.get(id=class_id)
                students = Student.objects.filter(
                    roll_number=roll_number, 
                    class_name=class_obj
                ).order_by('id')
                
                self.stdout.write(
                    f'Class: {class_obj.name}, Roll: {roll_number}, Count: {count}'
                )
                
                if options['fix']:
                    # Keep the first student unchanged, modify others
                    for i, student in enumerate(students[1:], 1):
                        old_roll = student.roll_number
                        new_roll = f"{roll_number}-{i}"
                        student.roll_number = new_roll
                        student.save()
                        self.stdout.write(
                            f'  Updated student {student.name}: {old_roll} -> {new_roll}'
                        )
                else:
                    for student in students:
                        self.stdout.write(f'  - {student.name} (ID: {student.id})')
            
            except Class.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Class with ID {class_id} does not exist')
                )
        
        if not options['fix']:
            self.stdout.write(
                self.style.WARNING(
                    'Run with --fix to automatically resolve duplicates by adding suffixes'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Duplicate roll numbers have been fixed.')
            )
