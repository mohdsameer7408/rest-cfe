from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class BlogLimitOffsetPaginator(LimitOffsetPagination):
    default_limit = 2
    max_limit = 5


class BlogPageNumberPaginator(PageNumberPagination):
    page_size = 2

