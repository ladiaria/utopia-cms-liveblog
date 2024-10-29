from autoslug.fields import AutoSlugField
from photologue.models import Photo

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _, gettext
from django.utils.safestring import mark_safe
from django.utils.html import escape

from core.models import Publication
from cartelera.choices import LIVE_EMBED_EVENT_ACCESS_TYPES
from photologue_ladiaria.models import PhotoExtended


class Environment(models.Model):
    name = models.CharField(_("name"), max_length=64)
    url = models.URLField()

    class Meta:
        verbose_name = _("environment")

    def __str__(self):
        return self.name


def build_helptext(begin, true_to_title_false_to_desc=True):
    end = (
        gettext("the main title is applied.")
        if true_to_title_false_to_desc else gettext("the main description is applied.")
    )
    return mark_safe(begin) + escape("<head>") + gettext(' of the article page.<br>If left blank, ') + end


class LiveBlog(models.Model):
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    title = models.CharField(
        _("title"), max_length=128, unique=True, help_text=_("Enter a concise and descriptive title.")
    )
    slug = AutoSlugField(populate_from="title", always_update=True, null=True, blank=True, unique=True, max_length=200)
    description = models.CharField(_("description"), max_length=140, null=True, blank=True)
    alt_title = models.CharField(
        _("alternative title"),
        blank=True,
        null=True,
        max_length=200,
        help_text=build_helptext(_('Applies to title tag in the '))
    )
    alt_title_meta = models.CharField(
        _("alternative title for metadata"),
        blank=True,
        null=True,
        max_length=200,
        help_text=build_helptext(_('Applies to metadata: meta title, Open Graph and Schema in the '))
    )
    alt_desc_meta = models.TextField(
        _("alternative description for metadata"),
        blank=True,
        null=True,
        help_text=build_helptext(_('Applies to the content of the description meta tag in the '), False)
    )
    alt_desc_og_meta = models.TextField(
        _("alternative description for og metadata"),
        blank=True,
        null=True,
        help_text=build_helptext(_('Applies to metadata: Open Graph and Schema in the '), False)
    )
    url = models.URLField(help_text=_("The URL of the blog in the LiveBlog environment."))
    day = models.DateField(_("date"), default=timezone.now)
    location = models.CharField(_("location"), max_length=128)
    status = models.CharField(
        _("status"),
        max_length=8,
        choices=(("idle", _("idle")), ("to_begin", _("to begin")), ("active", _("active")), ("ended", _("ended"))),
        default="idle",
    )
    image = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name=_("photo"), blank=True, null=True)
    access_type = models.CharField(_("access"), max_length=1, choices=LIVE_EMBED_EVENT_ACCESS_TYPES, default='s')
    in_home = models.BooleanField(_("featured in home"), default=False)
    notification = models.BooleanField(
        _("notification"),
        default=False,
        help_text=_(
            "If checked and the blog status is active or to begin, shows an alert related to this blog in articles "
            "and publication home pages."
        ),
    )
    notification_text = models.CharField(_("notification text"), max_length=255, null=True, blank=True)
    notification_url = models.URLField(_("notification url"), null=True, blank=True)
    notification_target_pubs = models.ManyToManyField(
        Publication,
        verbose_name=_("notification target publications"),
        blank=True,
        help_text=_("Alerts will be shown only in the pages (homes/articles) related to the publications selected."),
    )

    class Meta:
        verbose_name = _("live blog")
        verbose_name_plural = _("live blogs")
        ordering = ("-day",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("liveblog-detail", kwargs={"slug": self.slug})

    def is_free(self):
        return self.access_type == 'f'

    def clean(self):
        from django.core.exceptions import ValidationError

        inhome_now = LiveBlog.objects.filter(in_home=True)
        if self.in_home:
            if self.status != "active":
                raise ValidationError(_('Only active blogs can be featured in home.'))
            elif inhome_now.exclude(id=self.id) if self.id else inhome_now:
                # Don't allow more than one instance in home
                raise ValidationError(
                    _('There is another blog in home now, more than one blog in home is not allowed.')
                )

    def has_image(self):
        try:
            return bool(self.image)
        except PhotoExtended.DoesNotExist:
            return False

    def image_image_file_exists(self):
        try:
            result = self.has_image() and bool(self.image.image.file)
        except IOError:
            result = False
        return result

    def image_render_allowed(self):
        return self.image_image_file_exists() and self.image.is_public

    def save(self, *args, **kwargs):
        self.full_clean()  # calls self.clean() as well cleans other fields
        save_result = super().save(*args, **kwargs)
        self.refresh_from_db()
        new_url = self.get_absolute_url()
        # add to history the potential new url
        if not LiveBlogUrlHistory.objects.filter(liveblog=self, absolute_url=new_url).exists():
            LiveBlogUrlHistory.objects.create(liveblog=self, absolute_url=new_url)
        return save_result


class LiveBlogUrlHistory(models.Model):
    liveblog = models.ForeignKey(LiveBlog, on_delete=models.CASCADE)
    absolute_url = models.URLField(max_length=500, db_index=True)

    class Meta:
        unique_together = ('liveblog', 'absolute_url')
