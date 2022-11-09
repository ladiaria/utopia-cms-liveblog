from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.decorators.cache import never_cache

from utopia_cms_liveblog.models import LiveBlog


class LiveBlogList(ListView):
    model = LiveBlog


class LiveBlogDetail(DetailView):
    model = LiveBlog
    query_pk_and_slug = True


@never_cache
def notification_closed(request, liveblog_id):
    closed = request.session.get('liveblog_notifications_closed', set())
    closed.add(int(liveblog_id))
    request.session['liveblog_notifications_closed'] = closed
    return HttpResponse()
