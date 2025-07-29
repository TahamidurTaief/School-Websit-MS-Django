# web/context_processors.py

from .models import SchoolInfo

def school_info_processor(request):
    """
    Makes the primary SchoolInfo object available to all templates
    that use RequestContext.
    """
    school_info = SchoolInfo.objects.first()
    return {'school_info': school_info}