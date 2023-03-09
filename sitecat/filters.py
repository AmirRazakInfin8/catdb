import django_filters

import pprint
from django_elasticsearch_dsl import Document
from .models import Human, Home, Cat, Breed
from elasticsearch_dsl import Search, Q
from .documents import HumanDocument


class ElasticSearchFilter(django_filters.Filter):
    def __init__(self, document_class: Document, fields=None, **kwargs):
        self.document_class = document_class
        self.fields = fields
        super().__init__(**kwargs)

    def filter(self, qs, value):
        if not value or not self.fields:
            return qs

        search = Search(index=self.document_class._index._name)
        search = search.query(
            Q('multi_match', query=value, fields=self.fields))

        response = search.execute()
        ids = [hit.meta.id for hit in response]

        return qs.filter(id__in=ids)


class HumanFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="search_method")
    id = django_filters.rest_framework.NumberFilter(
        field_name="id", required=False)

    def search_method(self, qs, name, value):
        if not value:
            return qs

        search = Search(index=HumanDocument._index._name)
        search = search.query(
            Q('multi_match', query=value, fields=['name', 'description']))

        response = search.execute()
        ids = [hit.meta.id for hit in response]

        return qs.filter(id__in=ids)

    class Meta:
        model = Human
        fields = {
            "name": ("iexact", "icontains"),
            "gender": ("exact",),
            "description": ("icontains",),
            "birth_date": ("gte", "lte")
        }


class HomeFilter(django_filters.FilterSet):
    id = django_filters.rest_framework.NumberFilter(
        field_name="id", required=False)

    class Meta:
        model = Home
        fields = {
            "name": ("iexact", "icontains"),
            "address": ("iexact", "icontains"),
            "house_type": ("exact", )
        }


class CatFilter(django_filters.FilterSet):
    id = django_filters.rest_framework.NumberFilter(
        field_name="id", required=False)

    class Meta:
        model = Cat
        fields = {
            "name": ("iexact", "icontains"),
            "gender": ("exact",),
            "description": ("icontains",),
            "birth_date": ("gte", "lte")
        }


class BreedFilter(django_filters.FilterSet):
    id = django_filters.rest_framework.NumberFilter(
        field_name="id", required=False)

    class Meta:
        model = Breed
        fields = {
            "name": ("iexact", "icontains"),
            "origin": ("iexact", "icontains"),
            "description": ("icontains",),

        }
