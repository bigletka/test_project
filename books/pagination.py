from rest_framework.pagination import LimitOffsetPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    def get_limit(self, request):
        if 'limit' in request.query_params:
            return super().get_limit(request)
        return None
