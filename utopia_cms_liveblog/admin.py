from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from utopia_cms_liveblog.models import Environment, LiveBlog


@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_editable = ("name", "url")


@admin.register(LiveBlog)
class LiveBlogAdmin(admin.ModelAdmin):
    list_display = ("day", "environment", "title", "status", "in_home", "notification")
    raw_id_fields = ("image", )
    list_filter = ("status", )
    date_hierarchy = "day"


