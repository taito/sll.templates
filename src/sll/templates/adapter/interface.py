from five import grok
from plone.registry.interfaces import IRegistry
from sll.templates.interfaces import IEventFeed
from sll.templates.interfaces import IFolderFeed
from sll.templates.interfaces import INewsFeed
from sll.templates.interfaces import IAdapter
from sll.templates.interfaces import ITopPageMainFeed
from zope.component import getUtility
from zope.interface import Interface


class Adapter(grok.Adapter):
    """Adapter for root object."""

    grok.context(Interface)
    grok.provides(IAdapter)

    def get_feed_number(self, interface):
        records = getUtility(IRegistry).forInterface(interface)
        if interface == ITopPageMainFeed:
            name = 'main'
        elif interface == INewsFeed:
            name = 'news'
        elif interface == IEventFeed:
            name = 'event'
        elif interface == IFolderFeed:
            name = 'folder'
        else:
            raise ValueError('Not correct interface.')
        attr = '{}_feed_number'.format(name)
        number = getattr(self.context, attr, None)
        if number is not None:
            return number
        else:
            return records.number
