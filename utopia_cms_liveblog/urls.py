from django.urls import path, re_path
from utopia_cms_liveblog.views import (
    liveblog_list, LiveBlogDetail, notification, notification_closed, notification_others_closed
)


def get_urlpatterns(detail_class=LiveBlogDetail):
    return [
        path('', liveblog_list),
        re_path(r'^notification/(?P<publication_slug>[-\w]+)/$', notification, name='liveblog-notification'),
        path('liveblog/<int:liveblog_id>/closed/', notification_closed, name='liveblog-notification-closed'),
        path(
            'liveblog_others/<int:liveblog_id>/closed/',
            notification_others_closed,
            name='liveblog-notification-others-closed',
        ),
        re_path(r'^(?P<slug>[-\w]+)/$', detail_class.as_view(), name="liveblog-detail"),
    ]


urlpatterns = get_urlpatterns()
