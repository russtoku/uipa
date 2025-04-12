from django.urls import re_path

from .views import show_foilaw

urlpatterns = [
    re_path(r"^(?P<slug>[-\w]+)/$", show_foilaw, name="publicbody-foilaw-show"),
]
