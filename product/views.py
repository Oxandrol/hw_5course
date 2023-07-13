from django.db.models import Avg, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from product.models import Product, Review, Category, Tag
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer, TagSerializer, \
    ProductValidateSerializer, CategoryValidateSerializer, ReviewValidateSerializer, TagValidateSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


class ProductsListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def post(self, request, *args, **kwargs):
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')
        product = Product.objects.create(title=title, description=description, price=price, category_id=category_id)
        product.tags.set(tags)
        product.save()
        return Response(status=status.HTTP_201_CREATED)


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def put(self, request, pk, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        serializer = ProductValidateSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')
        product.tags.set(tags)
        product.save()
        return Response(status=status.HTTP_200_OK)


class ReviewListAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def post(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        product_id = serializer.validated_data.get('product_id')
        review = Review.objects.create(text=text, stars=stars, product_id=product_id)
        review.save()
        return Response(status=status.HTTP_201_CREATED)


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def put(self, request, pk, *args, **kwargs):
        review = Review.objects.get(pk=pk)
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.product_id = serializer.validated_data.get('product_id')
        review.save()
        return Response(status=status.HTTP_200_OK)


class CategoryListAPIView(APIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination

    def get(self, request):
        categories = Category.objects.all()
        products_count = Category.objects.aggregate(count_products=Count('category'))
        data_dict = CategorySerializer(categories, many=True).data
        return Response(data=[data_dict, products_count])

    def post(self, request, *args, **kwargs):
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get('name')
        category = Category.objects.create(name=name)
        category.save()
        return Response(status=status.HTTP_201_CREATED)


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def put(self, request, pk, *args, **kwargs):
        category = Category.objects.get(pk=pk)
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category.name = serializer.validated_data.get('name')
        category.save()
        return Response(status=status.HTTP_200_OK)


class TagsListAPIView(ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = PageNumberPagination

    def post(self, request, *args, **kwargs):
        serializer = TagValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get('name')
        tag = Tag.objects.create(name=name)
        tag.save()
        return Response(status=status.HTTP_201_CREATED)


class TagDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def put(self, request, pk, *args, **kwargs):
        tag = Tag.objects.get(pk=pk)
        serializer = TagValidateSerializer(tag, data=request.data)
        serializer.is_valid(raise_exception=True)
        tag.name = serializer.validated_data.get('name')
        tag.save()


class ProductsReviewsAPIView(APIView):
    def get(self, request):
        products_reviews = Review.objects.all()
        avg_stars = Review.objects.aggregate(avg=Avg('stars'))
        data_dict = ReviewSerializer(products_reviews, many=True).data
        return Response(data=[data_dict, avg_stars])
