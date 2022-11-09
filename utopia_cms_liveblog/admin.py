from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from utopia_cms_liveblog.models import Environment, LiveBlog


class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_editable = ("name", "url")


class LiveBlogAdmin(admin.ModelAdmin):
    list_display = ("id", "environment", "title", "url", "access_type", "in_home", "notification")
    list_editable = ("title", )


admin.site.register(Environment, EnvironmentAdmin)
admin.site.register(LiveBlog, LiveBlogAdmin)
