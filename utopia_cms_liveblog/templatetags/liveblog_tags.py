from __future__ import unicode_literals

from django import template
from django.template.loader import render_to_string


register = template.Library()


@register.simple_tag(takes_context=True)
def render_liveblog_notification(context):
    try:
        liveblog = context['liveblog']  # if present, is the one with in_home = True (by context processor definition)
        if (
            liveblog.notification
            and liveblog.id not in context['request'].session.get('liveblog_notifications_closed', set())
        ):
            return render_to_string('utopia_cms_liveblog/liveblog_notification.html', context.flatten())
    except KeyError:
        pass
    return ""


@register.simple_tag
def liveblog_embed_code(liveblog_obj):
    return render_to_string('utopia_cms_liveblog/liveblog_embed_code.html', {"object": liveblog_obj})
