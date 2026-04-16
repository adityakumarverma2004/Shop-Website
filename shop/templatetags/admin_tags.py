from django import template
from shop.models import ContactMessage

register = template.Library()

@register.simple_tag
def get_recent_messages(count=5):
    """
    Returns the most recent ContactMessage objects.
    Default count is 5.
    """
    return ContactMessage.objects.order_by('-created_at')[:count]
