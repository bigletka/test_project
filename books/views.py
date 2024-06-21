from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from .filters import BookFilter
from .models import Book, Favourite, Review
from .permissions import IsOwnerOrReadOnly
from .serializers import (BookDetailSerializer, BookListSerializer,
                          FavouriteSerializer, ReviewPerformSerializer)


class BookListView(generics.ListAPIView):
    parser_classes = (MultiPartParser, FormParser)
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name', 'genre__name']
    ordering_fields = ['publication_date']

    def get_serializer_context(self):
        context = super(BookListView, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class BookDetailView(generics.RetrieveAPIView):
    parser_classes = (MultiPartParser, FormParser)
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    lookup_field = 'id'

    def get_serializer_context(self):
        context = super(BookDetailView, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class FavoriteViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FavouriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ReviewPerformSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
