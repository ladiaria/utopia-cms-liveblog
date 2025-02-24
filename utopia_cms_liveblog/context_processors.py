# -*- coding: utf-8 -*-
from utopia_cms_liveblog.models import LiveBlog

from .apps import UtopiaCmsLiveblogConfig as liveblog_settings


def liveblog(request):
    result = {"liveblog_base_path": liveblog_settings.BASE_PATH}
    if request.path == "/":
        # the liveblog ctx var only makes sense in home page (path=/)
        try:
            lb = LiveBlog.objects.get(in_home=True)
        except (LiveBlog.DoesNotExist, LiveBlog.MultipleObjectsReturned):
            pass
        else:
            granted = True
            if lb.access_type == "s":
                granted = hasattr(request.user, "subscriber") and request.user.subscriber.is_subscriber_any()
            if granted:
                result["liveblog"] = lb
    if LiveBlog.objects.filter(status__in=["active", "to_begin"], notification=True).exists():
        result["load_liveblog_notification_js"] = True
    return result
