from django.conf.urls import url
from utopia_cms_liveblog.views import (
    liveblog_list, LiveBlogDetail, notification, notification_closed, notification_others_closed
)


urlpatterns = [
    url(r'^$', liveblog_list),
    url(r'^notification/(?P<publication_slug>[-\w]+)/$', notification, name='liveblog-notification'),
    url(r'^liveblog/(?P<liveblog_id>\d+)/closed/$', notification_closed, name='liveblog-notification-closed'),
    url(
        r'^liveblog_others/(?P<liveblog_id>\d+)/closed/$',
        notification_others_closed,
        name='liveblog-notification-others-closed',
    ),
    url(r'^(?P<slug>[-\w]+)/$', LiveBlogDetail.as_view(), name="liveblog-detail"),
]
