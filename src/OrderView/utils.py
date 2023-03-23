from rest_framework.pagination import PageNumberPagination


class OrderViewPaginnator(PageNumberPagination):
    page_size = 50
