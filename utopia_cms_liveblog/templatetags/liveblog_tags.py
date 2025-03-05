from django import template
from django.template.loader import render_to_string


register = template.Library()


@register.simple_tag
def liveblog_embed_code(liveblog_obj, disable_iframe_resizer=False, is_frontpage=False, allowAttrs=False):
    return render_to_string(
        'utopia_cms_liveblog/liveblog_embed_code.html',
        {"object": liveblog_obj, "disable_iframe_resizer": disable_iframe_resizer, "is_frontpage": is_frontpage, "allowAttrs": allowAttrs},
    )
