from django.contrib import admin
from django.forms import ModelForm, TextInput
from .models import Environment, LiveBlog


@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_editable = ("name", "url")


class LiveBlogAdminForm(ModelForm):

    class Meta:
        widgets = dict((f, TextInput(attrs={'size': 128})) for f in ("title", 'description', "notification_text"))


@admin.register(LiveBlog)
class LiveBlogAdmin(admin.ModelAdmin):
    form = LiveBlogAdminForm
    list_display = ("day", "environment", "title", "status", "in_home", "notification")
    raw_id_fields = ("image", )
    list_filter = ("status", )
    date_hierarchy = "day"
