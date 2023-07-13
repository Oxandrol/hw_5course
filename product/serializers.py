from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from product.models import Product, Review, Category, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'name'.split()


class TagValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'name'.split()


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField()


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False)
    price = serializers.IntegerField()
    category_id = serializers.IntegerField(min_value=1)
    tags = serializers.ListField(child=serializers.IntegerField())


    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category does not exist')
        return category_id

    def validate_tags(self, tags):
        missing = []
        for i, tag_id in enumerate(tags):
            try:
                Tag.objects.get(id=tag_id)
            except Tag.DoesNotExist:
                missing.append(tag_id)
        if missing:
            raise ValidationError({"tag does not exist": missing})
        return tags


class ProductSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = 'id title description price category tags'.split()


class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Review
        fields = 'product text stars'.split()


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField()
    stars = serializers.IntegerField()
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        try:
            Review.objects.get(id=product_id)
        except Review.DoesNotExist:
            raise ValidationError('Review does not exist')
        return product_id

