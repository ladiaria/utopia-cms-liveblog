from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UtopiaCmsLiveblogConfig(AppConfig):
    name = 'utopia_cms_liveblog'
    verbose_name = _("Live Blogs")
    BASE_PATH = "liveblogs"
