from django_filters import filters, FilterSet
from company import models


class LabelFilterSet(FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = models.Label
        fields = ["name"]


class ProjectCategoryFilterSet(FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = models.ProjectCategory
        fields = ["name"]


class ProjectFilterSet(FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    description = filters.CharFilter(lookup_expr="icontains")
    category = filters.CharFilter(lookup_expr="icotains", field_name="category__name")
