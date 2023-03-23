from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class OrderViewPaginnator(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ("records_on_page", self.page_size),
            ("all_page_count", (self.page.paginator.count // self.page_size + 1 if self.page.paginator.count % self.page_size != 0 else self.page.paginator.count // self.page_size)),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
        ]))
