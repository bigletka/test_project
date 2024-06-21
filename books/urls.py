from django.urls import path
from .views import BookListView, BookDetailView, FavoriteViewSet, ReviewViewSet


favorite_list = FavoriteViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

favorite_detail = FavoriteViewSet.as_view({
    'delete': 'destroy'
})

review_list = ReviewViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

review_detail = ReviewViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:id>/', BookDetailView.as_view(), name='book-detail'),
    path('favourites/', favorite_list, name='favorite-list'),
    path('favourites/<int:pk>/', favorite_detail, name='favorite-detail'),
    path('reviews/', review_list, name='review-list'),
    path('reviews/<int:pk>/', review_detail, name='review-detail'),
]
