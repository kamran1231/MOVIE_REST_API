from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'p'
    last_page_strings = ['end']


class WatchListLOPaginaton(LimitOffsetPagination):
    default_limit = 5


class WatchListCURPagination(CursorPagination):
    page_size = 5