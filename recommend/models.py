from django.db import models
from django.utils import timezone

from accounts.models import Tag
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):
    category_name = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % (self.category_name)

    class Meta:
        ordering = ['-created_at']


class Product(models.Model):
    prod_no = models.AutoField(primary_key=True)
    prod_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, default="1")
    prod_name = models.CharField(max_length=100, null=False)
    prod_manufacturer = models.CharField(max_length=30)
    prod_price = models.CharField(max_length=10, null=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%d. [%s]%s" % (self.prod_no, self.prod_manufacturer, self.prod_name)

    class Meta:
        ordering = ['-updated_at']


class ProductImage(models.Model):
    prod_img_no = models.AutoField(primary_key=True)
    prod_no = models.ForeignKey(Product, on_delete=models.CASCADE)
    prod_img_file_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at']


class ProductTag(models.Model):
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class SearchLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Favorite(models.Model):
    fav_user = models.ForeignKey(User, on_delete=models.CASCADE)
    fav_prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    fav_created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fav_created_at']
