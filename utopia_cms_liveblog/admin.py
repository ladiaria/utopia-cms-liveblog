from django.contrib import admin
from django.forms import ModelForm, TextInput
from django.utils.translation import gettext_lazy as _

from .models import Environment, LiveBlog


@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_editable = ("name", "url")


class LiveBlogAdminForm(ModelForm):

    class Meta:
        widgets = dict(
            (f, TextInput(attrs={'size': 128})) for f in (
                "title",
                'description',
                "notification_text",
                "alt_title",
                "alt_title_meta",
                "alt_desc_meta",
                "alt_desc_og_meta",
            )
        )


@admin.register(LiveBlog)
class LiveBlogAdmin(admin.ModelAdmin):
    form = LiveBlogAdminForm
    list_display = ("day", "environment", "title", "status", "in_home", "notification")
    raw_id_fields = ("image",)
    list_filter = ("status",)
    date_hierarchy = "day"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "environment",
                    "title",
                    "description",
                    "url",
                    ("day", "location"),
                    ("status", "image"),
                    ("access_type", "in_home", "notification"),
                    "notification_text",
                    "notification_url",
                    "notification_target_pubs",
                )
            },
        ),
        (
            _("Metadata"),
            {
                "fields": ("alt_title", "alt_title_meta", "alt_desc_meta", "alt_desc_og_meta"),
                "classes": ("collapse",),
            },
        ),
    )
