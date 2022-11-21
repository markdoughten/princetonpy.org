from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from meetings.models import Meeting


class CustomAtomFeed(Atom1Feed):
    """
    Create a type of RSS feed that has content elements.
    """

    def root_attributes(self):
        attrs = super(CustomAtomFeed, self).root_attributes()
        return attrs

    def add_item_elements(self, handler, item):
        super(CustomAtomFeed, self).add_item_elements(handler, item)

        # 'content' is added to the item below, in item_extra_kwargs()
        # It's populated in item_your_custom_field(). Here we're creating
        # the <content> element and adding it to our feed xml
        if item['content'] is not None:
            handler.addQuickElement(u'content', item['content'])


class RecentAnnouncementsFeed(Feed):
    title = "Princeton Python User Group announcements"
    link = "/newsletter/princetonpy/archive/"
    description = "Announcements sent out by the Princeton Python User Group"

    def items(self):
        return Meeting.objects.order_by('-date')[:5]

    def item_title(self, item):
        return item.title

    def item_subtitle(self, item):
        return item.short_description

    def item_content(self, item):
        return item.announcement
