# -*- coding: utf-8 -*-
from utopia_cms_liveblog.models import LiveBlog

from .apps import UtopiaCmsLiveblogConfig as liveblog_settings


def liveblog(request):
    result = {"liveblog_base_path": liveblog_settings.BASE_PATH}
    try:
        result["liveblog"] = LiveBlog.objects.get(in_home=True)
    except (LiveBlog.DoesNotExist, LiveBlog.MultipleObjectsReturned):
        pass
    return result
