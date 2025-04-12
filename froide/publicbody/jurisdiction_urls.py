from django.urls import path, re_path
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _

from .views import show_jurisdiction


urlpatterns = [
    path("", show_jurisdiction, name="publicbody-show_jurisdiction"),
    # Translators: URL part
    re_path(r"^%s/$" % _('entity'),
        lambda r, slug: HttpResponseRedirect(
            reverse("publicbody-list", kwargs={'jurisdiction': slug})),
        name='show-pb_jurisdiction'),
    # Translators: URL part
    re_path(r"^%s/$" % _('entities'), lambda r, slug: HttpResponseRedirect(
            reverse("publicbody-list", kwargs={'jurisdiction': slug}))),
]
