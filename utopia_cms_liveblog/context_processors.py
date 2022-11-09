# -*- coding: utf-8 -*-
from utopia_cms_liveblog.models import LiveBlog


def liveblog(request):
    try:
        return {"liveblog": LiveBlog.objects.get(in_home=True)}
    except (LiveBlog.DoesNotExist, LiveBlog.MultipleObjectsReturned):
        return {}
