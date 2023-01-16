# from django_filters import DateTimeFromToRangeFilter, FilterSet

# from .models import History


# class FilterDateRange(FilterSet):
#     entry_date = DateTimeFromToRangeFilter()
    
#     class Meta:
#         model = History
#         fields = ['entry_date', ]


import django_filters
from psycopg2.extras import DateRange


class DateExactRangeWidget(django_filters.widgets.DateRangeWidget):
    """Date widget to help filter by *_start and *_end."""
    suffixes = ['start', 'end']


class DateExactRangeField(django_filters.fields.DateRangeField):
    widget = DateExactRangeWidget

    def compress(self, data_list):
        if data_list:
            start_date, stop_date = data_list
            return DateRange(start_date, stop_date)


class DateExactRangeFilter(django_filters.Filter):
    """
    Filter to be used for Postgres specific Django field - DateRangeField.
    https://docs.djangoproject.com/en/2.1/ref/contrib/postgres/fields/#daterangefield
    """
    field_class = DateExactRangeField