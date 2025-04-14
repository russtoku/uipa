from django.urls import reverse
from django.urls import include, path, re_path
from django.utils.translation import pgettext
from django.shortcuts import redirect

from .models import FoiRequest
from .views import list_requests, list_unchecked, submit_request


urlpatterns = [
    re_path(r'^%s/$' % pgettext('URL part', 'not-foi'), list_requests,
        kwargs={'not_foi': True}, name='foirequest-list_not_foi'),

    # Old feed URL
    re_path(r'^%s/feed/$' % pgettext('URL part', 'latest'),
        lambda r: redirect(reverse('foirequest-list_feed_atom'), permanent=True),
        name='foirequest-feed_latest_atom'),
    re_path(r'^%s/rss/$' % pgettext('URL part', 'latest'),
        lambda r: redirect(reverse('foirequest-list_feed'), permanent=True),
        name='foirequest-feed_latest'),

    path('unchecked/', list_unchecked, name='foirequest-list_unchecked'),
    # Translators: part in /request/to/public-body-slug URL
    path('submit', submit_request, name='foirequest-submit_request'),
]


foirequest_urls = [
    path('', list_requests, name='foirequest-list'),
    path('feed/', list_requests,
        kwargs={'feed': 'atom'}, name='foirequest-list_feed_atom'),
    path('rss/', list_requests,
        kwargs={'feed': 'rss'}, name='foirequest-list_feed'),

    # Translators: part in request filter URL
    re_path(r'^%s/(?P<topic>[-\w]+)/$' % pgettext('URL part', 'topic'),
        list_requests, {}, 'foirequest-list'),
    re_path(r'^%s/(?P<topic>[-\w]+)/feed/$' % pgettext('URL part', 'topic'),
        list_requests, kwargs={'feed': 'atom'}, name='foirequest-list_feed_atom'),
    re_path(r'^%s/(?P<topic>[-\w]+)/rss/$' % pgettext('URL part', 'topic'),
        list_requests, kwargs={'feed': 'rss'}, name='foirequest-list_feed'),

    # Translators: part in request filter URL
    re_path(r'^%s/(?P<tag>[-\w]+)/$' % pgettext('URL part', 'tag'), list_requests,
        name='foirequest-list'),
    re_path(r'^%s/(?P<tag>[-\w]+)/feed/$' % pgettext('URL part', 'tag'),
        list_requests, kwargs={'feed': 'atom'}, name='foirequest-list_feed_atom'),
    re_path(r'^%s/(?P<tag>[-\w]+)/rss/$' % pgettext('URL part', 'tag'),
        list_requests, kwargs={'feed': 'rss'}, name='foirequest-list_feed'),

    # Translators: part in request filter URL
    re_path(r'^%s/(?P<public_body>[-\w]+)/$' % pgettext('URL part', 'to'),
        list_requests, name='foirequest-list'),
    re_path(r'^%s/(?P<public_body>[-\w]+)/feed/$' % pgettext('URL part', 'to'),
        list_requests, kwargs={'feed': 'atom'}, name='foirequest-list_feed_atom'),
    re_path(r'^%s/(?P<public_body>[-\w]+)/rss/$' % pgettext('URL part', 'to'),
        list_requests, kwargs={'feed': 'rss'}, name='foirequest-list_feed'),

] + [re_path(r'^(?P<status>%s)/$' % str(urlinfo[0]), list_requests,
        name='foirequest-list') for urlinfo in FoiRequest.get_status_url()
] + [re_path(r'^(?P<status>%s)/feed/$' % str(urlinfo[0]), list_requests,
        kwargs={'feed': 'atom'}, name='foirequest-list_feed_atom') for urlinfo in FoiRequest.get_status_url()
] + [re_path(r'^(?P<status>%s)/rss/$' % str(urlinfo[0]), list_requests,
        kwargs={'feed': 'rss'}, name='foirequest-list_feed') for urlinfo in FoiRequest.get_status_url()]

urlpatterns += foirequest_urls

urlpatterns += [
    re_path(r'^(?P<jurisdiction>[-\w]+)/', include(foirequest_urls))
]
