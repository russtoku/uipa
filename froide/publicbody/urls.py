from django.urls import path, re_path
from django.utils.translation import pgettext

from .views import confirm, import_csv, index


urlpatterns = [
    path("confirm/", confirm, name="publicbody-confirm"),
    path("import/", import_csv, name="publicbody-import"),

    path("", index, name="publicbody-list"),
    # Translators: part in Public Body URL
    re_path(r"^%s/(?P<topic>[-\w]+)/$" % pgettext('URL part', 'topic'),
            index, name="publicbody-list"),
    re_path(r"^(?P<jurisdiction>[-\w]+)/$",
            index, name="publicbody-list"),
    # Translators: part in Public Body URL
    re_path(r"^(?P<jurisdiction>[-\w]+)/%s/(?P<topic>[-\w]+)/$" % pgettext('URL part', 'topic'),
            index, name="publicbody-list"),
]
