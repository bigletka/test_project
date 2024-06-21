import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    publication_date_start = django_filters.DateFilter(
        field_name="publication_date",
        lookup_expr='gte'
        )

    publication_date_end = django_filters.DateFilter(
        field_name="publication_date",
        lookup_expr='lte'
        )

    class Meta:
        model = Book
        fields = ['author', 'genre', 'publication_date_start',
                  'publication_date_end']
