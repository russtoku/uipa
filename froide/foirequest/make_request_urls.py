from django.urls import path, re_path
from django.utils.translation import pgettext

from .views import make_request, submit_request


urlpatterns = [
    # Translators: part in /request/to/public-body-slug URL
    path('', make_request, name='foirequest-make_request'),
    re_path(r'^%s/(?P<public_body_id>\d+)/$' % pgettext('URL part', 'to'),
            make_request, name='foirequest-make_request'),
    re_path(r'^%s/(?P<public_body>[-\w]+)/$' % pgettext('URL part', 'to'),
            make_request, name='foirequest-make_request'),
    re_path(r'^%s/(?P<public_body>[-\w]+)/submit$' % pgettext('URL part', 'to'),
            submit_request, name='foirequest-submit_request'),
]
