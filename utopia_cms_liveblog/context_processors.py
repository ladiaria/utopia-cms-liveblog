# -*- coding: utf-8 -*-
from utopia_cms_liveblog.models import LiveBlog

from .apps import UtopiaCmsLiveblogConfig as liveblog_settings


def liveblog(request):
    result = {"liveblog_base_path": liveblog_settings.BASE_PATH}
    try:
        result["liveblog"] = LiveBlog.objects.get(in_home=True)
    except (LiveBlog.DoesNotExist, LiveBlog.MultipleObjectsReturned):
        pass
    if LiveBlog.objects.filter(status__in=["active", "to_begin"], notification=True).exists():
        result["load_liveblog_notification_js"] = True
    return result
