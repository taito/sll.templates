from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager


class ISllTemplatesLayer(Interface):
    """Marker interface for browserlayer."""


class ITopPageFeed(Interface):
    """Marker interface for top page feed."""


class IMicroSiteFeed(Interface):
    """Marker interface for micro site feed."""


class IFeedViewletManager(IViewletManager):
    """"A viewlet manager for Feed."""


class ITopViewletManager(IFeedViewletManager):
    """A viewlet manager for Portal Top Page."""


class ISimpleFeedViewletManager(IViewletManager):
    """Base Simple Feed manager for News and Events feed."""


class INewsFeedViewletManager(ISimpleFeedViewletManager):
    """News Feed Viewlet Manager."""


class IEventsFeedViewletManager(ISimpleFeedViewletManager):
    """Events Feed Viewlet Manager."""


class IFooterViewletManager(IViewletManager):
    """Footer ViewletManager."""