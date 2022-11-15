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
    return render(request, "utopia_cms_liveblog/liveblog_list.html", {"pager": pager})


class LiveBlogDetail(DetailView):
    model = LiveBlog
    query_pk_and_slug = True


@never_cache
def notification_closed(request, liveblog_id):
    closed = request.session.get('liveblog_notifications_closed', set())
    closed.add(int(liveblog_id))
    request.session['liveblog_notifications_closed'] = closed
    return HttpResponse()
