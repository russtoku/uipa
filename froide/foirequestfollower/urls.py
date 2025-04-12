from django.urls import re_path
from django.utils.translation import pgettext

from .views import follow, confirm_follow, unfollow_by_link

urlpatterns = [
    re_path(r"^(?P<slug>[-\w]+)/follow/$", follow, name="foirequestfollower-follow"),

    re_path(r'^%s/(?P<follow_id>\d+)/(?P<check>[0-9a-f]{32})/$' %
        pgettext('URL part', 'confirm-follow'), confirm_follow,
        name='foirequestfollower-confirm_follow'),
    re_path(r'^%s/(?P<follow_id>\d+)/(?P<check>[0-9a-f]{32})/$' %
        pgettext('URL part', 'unfollow'), unfollow_by_link,
        name='foirequestfollower-confirm_unfollow'),
]
