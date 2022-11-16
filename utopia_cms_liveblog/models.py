from autoslug.fields import AutoSlugField
from photologue.models import Gallery, Photo

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cartelera.choices import LIVE_EMBED_EVENT_ACCESS_TYPES


class Environment(models.Model):
    name = models.CharField(_("name"), max_length=64)
    url = models.URLField()

    class Meta:
        verbose_name = _("environment")

    def __str__(self):
        return self.name


class LiveBlog(models.Model):
    environment = models.ForeignKey(Environment)
    title = models.CharField(_("title"), max_length=255, unique=True)
    slug = AutoSlugField(populate_from="title", always_update=True, null=True, blank=True)
    description = models.TextField(_("description"), null=True, blank=True)
    url = models.URLField()
    active = models.BooleanField(_("active"), default=False)
    image = models.ForeignKey(Photo, verbose_name=_("photo"), blank=True, null=True)
    access_type = models.CharField(_("access"), max_length=1, choices=LIVE_EMBED_EVENT_ACCESS_TYPES, default='s')
    in_home = models.BooleanField(_("featured in home"), default=False)
    notification = models.BooleanField(_("articles notification"), default=False)
    notification_text = models.CharField(_("notification text"), max_length=255, null=True, blank=True)
    notification_url = models.URLField(_("notification url"), null=True, blank=True)

    class Meta:
        verbose_name = _("live blog")
        verbose_name_plural = _("live blogs")

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
            if (inhome_now.exclude(id=self.id) if self.id else inhome_now):
                # Don't allow more than one instance in home
                raise ValidationError(_('Only one blog can be in home at the same time.'))

    def save(self, *args, **kwargs):
        self.full_clean()  # calls self.clean() as well cleans other fields
        return super(LiveBlog, self).save(*args, **kwargs)
