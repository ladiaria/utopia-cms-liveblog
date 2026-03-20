from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from . import DESCRIPTION, __version__

class UtopiaCmsLiveblogConfig(AppConfig):
    name = "utopia_cms_liveblog"
    verbose_name = _("Live Blogs")
    utopia_cms_integrated_info = (f"{name} v{__version__}", DESCRIPTION)
    BASE_PATH = "liveblogs"
