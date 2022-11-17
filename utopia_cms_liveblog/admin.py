from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from utopia_cms_liveblog.models import Environment, LiveBlog


class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_editable = ("name", "url")


class LiveBlogAdmin(admin.ModelAdmin):
    list_display = ("day", "environment", "title", "status", "url", "in_home", "notification")
    list_editable = ("title", )
    raw_id_fields = ("image", )
    list_filter = ("status", )
    date_hierarchy = "day"


admin.site.register(Environment, EnvironmentAdmin)
admin.site.register(LiveBlog, LiveBlogAdmin)
