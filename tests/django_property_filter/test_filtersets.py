
import pytest

from django_property_filter import (
    PropertyFilterSet,
    PropertyChoiceFilter,
    PropertyNumberFilter,
)

from django_filters import FilterSet

from property_filter.models import (
    Product,
    RangeFilterModel
)


def test_declare_implicit_filter_normal_fs_no_filters():
    class Fs(FilterSet):

        class Meta:
            model = RangeFilterModel
            exclude = ['number']
            property_fields = [('prop_number', PropertyNumberFilter, ['gte', 'exact'])]

    fs = Fs({'prop_number': 5}, queryset=RangeFilterModel.objects.all())

    assert len(fs.filters) == 0


def test_declare_explicit_filter_normal_fs():
    class Fs(FilterSet):

        prop_number = PropertyNumberFilter(field_name='prop_number', lookup_expr='exact')

        class Meta:
            model = RangeFilterModel
            exclude = ['number']

    fs = Fs({'prop_number': 5}, queryset=RangeFilterModel.objects.all())

    assert len(fs.filters) == 1
    assert fs.filters['prop_number'].model == RangeFilterModel
    assert fs.filters['prop_number'].parent == fs


def test_declare_implicit_filter_property_fs():
    class Fs(PropertyFilterSet):

        class Meta:
            model = RangeFilterModel
            exclude = ['number']
            property_fields = [('prop_number', PropertyNumberFilter, ['gte', 'exact'])]

    fs = Fs({'prop_number': 5}, queryset=RangeFilterModel.objects.all())

    assert len(fs.filters) == 2
    assert 'prop_number__gte' in fs.filters
    assert fs.filters['prop_number__gte'].lookup_expr == 'gte'
    assert fs.filters['prop_number__gte'].model == RangeFilterModel
    assert fs.filters['prop_number__gte'].parent == fs

    assert 'prop_number__exact' in fs.filters
    assert fs.filters['prop_number__exact'].lookup_expr == 'exact'
    assert fs.filters['prop_number__exact'].model == RangeFilterModel
    assert fs.filters['prop_number__exact'].parent == fs


def test_declare_explicit_filter_property_fs():
    class Fs(PropertyFilterSet):

        prop_number = PropertyNumberFilter(field_name='prop_number', lookup_expr='exact')

        class Meta:
            model = RangeFilterModel
            exclude = ['number']

    fs = Fs({'prop_number': 5}, queryset=RangeFilterModel.objects.all())

    assert len(fs.filters) == 1
    assert fs.filters['prop_number'].model == RangeFilterModel
    assert fs.filters['prop_number'].parent == fs


def test_declare_implicit_filter_multiple_properties_property_fs():
    class Fs(PropertyFilterSet):

        class Meta:
            model = Product
            exclude = ['name', 'price', 'del_line']
            property_fields = [
                ('prop_name', PropertyNumberFilter, ['gte']),
                ('prop_line_no', PropertyNumberFilter, ['exact'])
                ]

    fs = Fs({'prop_name': 5}, queryset=Product.objects.all())

    assert len(fs.filters) == 2
    assert 'prop_name__gte' in fs.filters
    assert fs.filters['prop_name__gte'].lookup_expr == 'gte'
    assert fs.filters['prop_name__gte'].model == Product
    assert fs.filters['prop_name__gte'].parent == fs

    assert 'prop_line_no__exact' in fs.filters
    assert fs.filters['prop_line_no__exact'].lookup_expr == 'exact'
    assert fs.filters['prop_line_no__exact'].model == Product
    assert fs.filters['prop_line_no__exact'].parent == fs


def test_invalid_implicit_class():
    class Fs(PropertyFilterSet):

        class Meta:
            model = RangeFilterModel
            exclude = ['number']
            property_fields = [('prop_number', RangeFilterModel, ['gte'])]

    with pytest.raises(ValueError):
        Fs({'prop_number': 5}, queryset=RangeFilterModel.objects.all())

def test_invalid_implicit_field_name():
    class Fs(PropertyFilterSet):

        class Meta:
            model = RangeFilterModel
            exclude = ['number']
            property_fields = [(None, PropertyNumberFilter, ['gte'])]

    with pytest.raises(ValueError):
        Fs({'prop_number': 5}, queryset=RangeFilterModel.objects.all())

def test_invalid_implicit_lookup_empty_list():
    class Fs(PropertyFilterSet):

        class Meta:
            model = RangeFilterModel
            exclude = ['number']
            property_fields = [('prop_number', PropertyNumberFilter, [])]

    with pytest.raises(ValueError):
        Fs({'prop_number': 5}, queryset=RangeFilterModel.objects.all())

def test_invalid_implicit_lookup_invalid_list():
    class Fs(PropertyFilterSet):

        class Meta:
            model = RangeFilterModel
            exclude = ['number']
            property_fields = [('prop_number', PropertyNumberFilter, None)]

    with pytest.raises(ValueError):
        Fs({'prop_number': 5}, queryset=RangeFilterModel.objects.all())

def test_disallowed_implicid_filter_created():

    class Fs(PropertyFilterSet):

        class Meta:
            model = Product
            exclude = ['name', 'price', 'del_line']
            property_fields = [
                ('prop_name', PropertyChoiceFilter, ['exact'])
                ]

    with pytest.raises(ValueError):
        Fs({'prop_name': '5'}, queryset=Product.objects.all())

