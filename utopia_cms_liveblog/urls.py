from django.conf.urls import url
from utopia_cms_liveblog.views import liveblog_list, LiveBlogDetail, notification_closed


urlpatterns = [
    url(r'^$', liveblog_list),
    url(r'^liveblog/(?P<liveblog_id>\d+)/closed/$', notification_closed, name='liveblog-notification-closed'),
    url(r'^(?P<slug>[-\w]+)/$', LiveBlogDetail.as_view(), name="liveblog-detail"),
]
