from autoslug.fields import AutoSlugField
from photologue.models import Photo

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import Publication
from cartelera.choices import LIVE_EMBED_EVENT_ACCESS_TYPES


class Environment(models.Model):
    name = models.CharField(_("name"), max_length=64)
    url = models.URLField()

    class Meta:
        verbose_name = _("environment")

    def __str__(self):
        return self.name


class LiveBlog(models.Model):
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=128, unique=True)
    slug = AutoSlugField(populate_from="title", always_update=True, null=True, blank=True)
    description = models.CharField(_("description"), max_length=140, null=True, blank=True)
    url = models.URLField()
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

    def save(self, *args, **kwargs):
        self.full_clean()  # calls self.clean() as well cleans other fields
        return super(LiveBlog, self).save(*args, **kwargs)
