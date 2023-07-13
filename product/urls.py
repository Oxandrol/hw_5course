from django.urls import path
from product import views

urlpatterns = [
    path('categories/', views.CategoryListAPIView.as_view()),
    path('categories/<int:pk>/', views.CategoryDetailAPIView.as_view()),
    path('products/', views.ProductsListAPIView.as_view()),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view()),
    path('reviews/', views.ReviewListAPIView.as_view()),
    path('reviews/<int:pk>/', views.ReviewDetailAPIView.as_view()),
    path('products/reviews/', views.ProductsReviewsAPIView.as_view()),
    path('tags/', views.TagsListAPIView.as_view()),
    path('tags/<int:pk>/', views.TagDetailAPIView.as_view())
]
