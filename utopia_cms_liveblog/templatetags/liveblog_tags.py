from django.conf import settings
from django import template
from django.template.loader import render_to_string


register = template.Library()


@register.simple_tag()
def liveblog_embed_code(
    liveblog_obj, disable_iframe_resizer=False, is_frontpage=False, allowAttrs=False, is_post_anchor=False
):
    query_params = []
    if is_frontpage:
        query_params.append('is_frontpage=1')
    if is_post_anchor:
        query_params.append('is_anchor=1')
    if liveblog_obj:
        query_params.append('liveblog_url=%s%s' % (settings.SITE_URL_SD, liveblog_obj.get_absolute_url()))
    query_params_str = '&'.join(query_params) if query_params else ''
    return render_to_string(
        'utopia_cms_liveblog/liveblog_embed_code.html',
        {
            "object": liveblog_obj,
            "disable_iframe_resizer": disable_iframe_resizer,
            "is_frontpage": is_frontpage,
            "allowAttrs": allowAttrs,
            "query_params_str": query_params_str,
        },
    )
