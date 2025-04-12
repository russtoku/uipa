from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

import floppyforms as forms

from froide.publicbody.models import (PublicBody,
    PublicBodyTag, TaggedPublicBody, FoiLaw, Jurisdiction)
from froide.helper.admin_utils import AdminTagAllMixIn
from froide.helper.widgets import TagAutocompleteTagIt
from froide.helper.csv_utils import export_csv_response


class PublicBodyAdminForm(forms.ModelForm):
    class Meta:
        model = PublicBody
        fields = '__all__'
        widgets = {
            'tags': TagAutocompleteTagIt(
                autocomplete_url=lambda: reverse('api_get_tags_autocomplete', kwargs={
                    'api_name': 'v1',
                    'resource_name': 'publicbody'}
                )),
        }


@admin.register(PublicBody)
class PublicBodyAdmin(admin.ModelAdmin, AdminTagAllMixIn):
    form = PublicBodyAdminForm

    prepopulated_fields = {
        "slug": ("name",),
        'classification_slug': ('classification',)
    }
    list_display = ('name', 'email', 'url', 'tag_list', 'classification', 'jurisdiction',)
    list_filter = ('tags', 'jurisdiction', 'classification')
    filter_horizontal = ('laws',)
    list_max_show_all = 5000
    search_fields = ['name', "description", 'classification']
    exclude = ('confirmed',)
    raw_id_fields = ('parent', 'root', '_created_by', '_updated_by')

    autocomplete_resource_name = 'publicbody'

    actions = ['export_csv', 'remove_from_index', 'tag_all']

    @admin.action(
        description=_("Export to CSV")
    )
    def export_csv(self, request, queryset):
        return export_csv_response(PublicBody.export_csv(queryset))

    @admin.action(
        description=_("Remove from search index")
    )
    def remove_from_index(self, request, queryset):
        from haystack import connections as haystack_connections

        for obj in queryset:
            for using in list(haystack_connections.connections_info.keys()):
                backend = haystack_connections[using].get_backend()
                backend.remove(obj)

        self.message_user(request, _("Removed from search index"))


@admin.register(FoiLaw)
class FoiLawAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'meta', 'jurisdiction',)
    list_filter = ('jurisdiction',)
    raw_id_fields = ('mediator',)
    filter_horizontal = ('combined',)


@admin.register(Jurisdiction)
class JurisdictionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ['hidden', 'rank']
    list_display = ['name', 'hidden', 'rank']


@admin.register(PublicBodyTag)
class PublicBodyTagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_topic", "rank"]
    list_filter = ['is_topic', 'rank']
    ordering = ["rank", "name"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(TaggedPublicBody)
class TaggedPublicBodyAdmin(admin.ModelAdmin):
    raw_id_fields = ('content_object', 'tag')


