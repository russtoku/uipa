from django.conf import settings

from haystack import indexes
from haystack import fields

try:
    from celery_haystack.indexes import CelerySearchIndex as SearchIndex
except ImportError:
    SearchIndex = indexes.SearchIndex

from .models import PublicBody

PUBLIC_BODY_BOOSTS = settings.FROIDE_CONFIG.get("public_body_boosts", {})


class PublicBodyIndex(SearchIndex, indexes.Indexable):
    text = fields.EdgeNgramField(document=True, use_template=True)
    name = fields.CharField(model_attr='name', boost=1.5)
    name_auto = fields.NgramField(model_attr='name')
    jurisdiction = fields.FacetCharField(model_attr='jurisdiction__name', default='')
    tags = fields.FacetMultiValueField()
    url = fields.CharField(model_attr='get_absolute_url')

    def get_model(self):
        return PublicBody

    def index_queryset(self, **kwargs):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.get_for_search_index()

    def prepare_tags(self, obj):
        return [t.name for t in obj.tags.all()]

    def prepare(self, obj):
        data = super().prepare(obj)
        if obj.classification in PUBLIC_BODY_BOOSTS:
            data['boost'] = PUBLIC_BODY_BOOSTS[obj.classification]
            print("Boosting {} at {:f}".format(obj, data['boost']))
        return data
