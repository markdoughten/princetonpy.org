from typing import Optional

from django.contrib.sites.models import Site
from django.template.loader import get_template
from newsletter.compat import get_context
from newsletter.models import Message


def render_message(message: Message) -> Optional[str]:
    variable_dict = {
        'site': Site.objects.get_current(),
        # 'submission': self,
        'message': message,
        # 'newsletter': message.newsletter,
        # 'date': self.publish_date,
        # 'STATIC_URL': settings.STATIC_URL,
        # 'MEDIA_URL': settings.MEDIA_URL
    }

    template = get_template('newsletter/message/feed.html')
    escaped_context = get_context(variable_dict)
    return template.render(escaped_context)
