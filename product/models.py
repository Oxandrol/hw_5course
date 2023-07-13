from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField(null=True, blank=True)
    stars = models.IntegerField(blank=True, validators=[MaxValueValidator(5), MinValueValidator(1)], default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')

    def __str__(self):
        return self.text

    # def product_reviews(self):
    #     if self.product:
    #         return self.text , self.stars
    #     else:
    #         return f"No reviews here"
