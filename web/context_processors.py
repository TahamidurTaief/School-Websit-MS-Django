# web/context_processors.py

from .models import SchoolInfo
from notice.models import Notice

def school_info_processor(request):
    """
    Makes the primary SchoolInfo object available to all templates
    that use RequestContext.
    """
    school_info = SchoolInfo.objects.first()
    latest_notice = Notice.objects.filter(is_active=True).first()
    return {
        'school_info': school_info,
        'latest_notice': latest_notice
    }

