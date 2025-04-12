from django.urls import path, re_path

from .feeds import FoiRequestFeed, FoiRequestFeedAtom
from .views import (shortlink, auth, show, suggest_public_body, set_public_body,
                    set_status, send_message, escalation_message, make_public,
                    set_law, set_tags, set_summary, add_postal_reply,
                    add_postal_reply_attachment, set_message_sender,
                    mark_not_foi, mark_checked, extend_deadline,
                    approve_attachment, approve_message, make_same_request,
                    resend_message, download_foirequest, redact_attachment)

urlpatterns = [
    path("<int:obj_id>", shortlink, name="foirequest-notsolonglink"),
    re_path(r"^(?P<obj_id>\d+)/auth/(?P<code>[0-9a-f]+)/$", auth, name="foirequest-longerauth"),
    re_path(r"^(?P<slug>[-\w]+)/$", show, name="foirequest-show"),
    re_path(r"^(?P<slug>[-\w]+)/suggest/public-body/$", suggest_public_body, name="foirequest-suggest_public_body"),
    re_path(r"^(?P<slug>[-\w]+)/set/public-body/$", set_public_body, name="foirequest-set_public_body"),
    re_path(r"^(?P<slug>[-\w]+)/set/status/$", set_status, name="foirequest-set_status"),
    re_path(r"^(?P<slug>[-\w]+)/send/message/$", send_message, name="foirequest-send_message"),
    re_path(r"^(?P<slug>[-\w]+)/escalation/message/$", escalation_message, name="foirequest-escalation_message"),
    re_path(r"^(?P<slug>[-\w]+)/make/public/$", make_public, name="foirequest-make_public"),
    re_path(r"^(?P<slug>[-\w]+)/set/law/$", set_law, name="foirequest-set_law"),
    re_path(r"^(?P<slug>[-\w]+)/set/tags/$", set_tags, name="foirequest-set_tags"),
    re_path(r"^(?P<slug>[-\w]+)/set/resolution/$", set_summary, name="foirequest-set_summary"),
    re_path(r"^(?P<slug>[-\w]+)/add/postal-reply/$", add_postal_reply, name="foirequest-add_postal_reply"),
    re_path(r"^(?P<slug>[-\w]+)/add/postal-reply/(?P<message_id>\d+)/$", add_postal_reply_attachment, name="foirequest-add_postal_reply_attachment"),
    re_path(r"^(?P<slug>[-\w]+)/(?P<message_id>\d+)/set/public-body/$", set_message_sender, name="foirequest-set_message_sender"),
    re_path(r"^(?P<slug>[-\w]+)/mark/not-foi/$", mark_not_foi, name="foirequest-mark_not_foi"),
    re_path(r"^(?P<slug>[-\w]+)/mark/checked/$", mark_checked, name="foirequest-mark_checked"),
    re_path(r"^(?P<slug>[-\w]+)/extend-deadline/$", extend_deadline, name="foirequest-extend_deadline"),
    re_path(r"^(?P<slug>[-\w]+)/approve/(?P<attachment>\d+)/$", approve_attachment, name="foirequest-approve_attachment"),
    re_path(r"^(?P<slug>[-\w]+)/approve/message/(?P<message>\d+)/$", approve_message, name="foirequest-approve_message"),
    re_path(r"^(?P<slug>[-\w]+)/make-same/(?P<message_id>\d+)/$", make_same_request, name="foirequest-make_same_request"),
    re_path(r"^(?P<slug>[-\w]+)/resend/$", resend_message, name="foirequest-resend_message"),
    re_path(r"^(?P<slug>[-\w]+)/download/$", download_foirequest, name="foirequest-download"),
    # Redaction
    re_path(r"^(?P<slug>[-\w]+)/redact/(?P<attachment_id>\d+)/$", redact_attachment, name="foirequest-redact_attachment"),
]

# Feed
urlpatterns += [
    re_path(r"^(?P<slug>[-\w]+)/feed/$", FoiRequestFeedAtom(), name="foirequest-feed_atom"),
    re_path(r"^(?P<slug>[-\w]+)/rss/$", FoiRequestFeed(), name="foirequest-feed")
]
