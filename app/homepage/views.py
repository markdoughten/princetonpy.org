import datetime

from dateutil.utils import today
from django.views.generic import TemplateView

from homepage.models import MeetingLink
from meetings.models import Meeting
from schedule import get_next_meeting_time, make_when


class Home(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            link_entry = MeetingLink.objects.latest("id")
            context["link_entry"] = link_entry
        except MeetingLink.DoesNotExist:
            pass
        try:
            meeting = Meeting.objects.filter(
                date__isnull=False, date__gte=today(datetime.timezone.utc)
            ).earliest("date")
            context["when"] = make_when(meeting.date)
        except Meeting.DoesNotExist:
            context["when"] = make_when(get_next_meeting_time())
        return context

class JitsiPage(TemplateView):
    template_name = "jitsi.html"
