from pathlib import PurePosixPath
from urllib.parse import urlparse
import requests

from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.views.generic import DetailView
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .apps import UtopiaCmsLiveblogConfig as liveblog_settings
from .models import LiveBlog


def liveblog_list(request):
    paginator = Paginator(LiveBlog.objects.all(), getattr(settings, "UTOPIA_CMS_LIVEBLOG_BLOGLIST_PAGINATED_BY", 10))
    page = request.GET.get('page')
    try:
        pager = paginator.page(page)
    except PageNotAnInteger:
        pager = paginator.page(1)
    except (EmptyPage, InvalidPage):
        pager = paginator.page(paginator.num_pages)
    return render(
        request,
        "utopia_cms_liveblog/liveblog_list.html",
        {"pager": pager, "tagline": getattr(settings, "UTOPIA_CMS_LIVEBLOG_BLOGLIST_TAGLINE", None)},
    )


class LiveBlogDetail(DetailView):
    model = LiveBlog
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        context, obj = super().get_context_data(**kwargs), self.get_object()
        try:
            api_url = "%s/api/client_blogs/%s/" % (
                obj.environment.url,
                PurePosixPath(urlparse(obj.url).path).parts[-1],
            )
            blog_meta = requests.get(api_url).json()
            # get only needed meta entries
            context["blog_meta"] = {
                "start_date": blog_meta.get("start_date"),
                "dateModified": blog_meta.get("last_updated_post", {}).get("_updated")
            }
            # most recent post info
            post_meta = requests.get(api_url + "posts").json()
            items = post_meta["_items"]  # TODO: all pages instead of 1st-only
            if len(items):
                context["blog_meta"]["posts"] = []
                for item in items:
                    item_refs = item["groups"][1]["refs"]
                    item_meta = {
                        "body": item_refs[0]["item"]["text"],
                        "created": item["_created"],
                        "updated": item["_updated"],
                        "author": item_refs[0]["item"]["original_creator"]["display_name"],
                    }
                    if len(item_refs) > 1:
                        image_src = item_refs[1]["item"]["meta"].get("media", {}).get("_url")
                        if image_src:
                            item_meta["image_src"] = image_src
                    context["blog_meta"]["posts"].append(item_meta)
        except Exception as exc:
            if settings.DEBUG:
                print(exc)
            if self.request.user.is_staff:
                warn_msg = _(
                    'Error trying to get the metadata from the liveblog origin environment. Check if the environment '
                    'is online and the blog URL is correctly set to this object.'
                )
                messages.warning(self.request, warn_msg)
        return context


@never_cache
def notification(request, publication_slug):
    # filter candidates
    liveblog, candidates = None, LiveBlog.objects.filter(
        status__in=("active", "to_begin"), notification=True, notification_target_pubs__slug=publication_slug
    )
    if candidates:
        # give priority to in-home blogs
        liveblog = candidates.filter(
            in_home=True
        ).exclude(id__in=request.session.get('liveblog_notifications_closed', set())).first()
        context = {"base_path": liveblog_settings.BASE_PATH}
        if not liveblog:
            # then to others
            liveblog = candidates.filter(
                in_home=False
            ).exclude(
                id__in=request.session.get('liveblog_notifications_others_closed', set())
            ).order_by("status").first()
            if liveblog:
                context["others"] = True
    if liveblog:
        context["liveblog"] = liveblog
        return render(request, 'utopia_cms_liveblog/liveblog_notification.html', context)
    else:
        return HttpResponse()


@never_cache
def notification_closed(request, liveblog_id):
    closed = request.session.get('liveblog_notifications_closed', set())
    closed.add(int(liveblog_id))
    request.session['liveblog_notifications_closed'] = closed
    return HttpResponse()


@never_cache
def notification_others_closed(request, liveblog_id):
    closed = request.session.get('liveblog_notifications_others_closed', set())
    closed.add(int(liveblog_id))
    request.session['liveblog_notifications_others_closed'] = closed
    return HttpResponse()
