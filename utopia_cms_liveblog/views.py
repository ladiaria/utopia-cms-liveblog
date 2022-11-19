from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.views.generic import DetailView
from django.views.decorators.cache import never_cache
from django.shortcuts import render

from .models import LiveBlog


def liveblog_list(request):
    paginator, page = Paginator(LiveBlog.objects.all(), 10), request.GET.get('page')
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


@never_cache
def notification(request, publication_slug):
    # filter candidates
    candidates = LiveBlog.objects.filter(
        status__in=("active", "to_begin"), notification=True, notification_target_pubs__slug=publication_slug
    )
    # give priority to in-home blogs
    liveblog, context = candidates.filter(
        in_home=True
    ).exclude(id__in=request.session.get('liveblog_notifications_closed', set())).first(), {}
    if not liveblog:
        # then to others
        liveblog = candidates.filter(
            in_home=False
        ).exclude(id__in=request.session.get('liveblog_notifications_others_closed', set())).order_by("status").first()
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
