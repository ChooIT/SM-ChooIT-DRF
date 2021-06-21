from django.db import models

from accounts.models import Tag
from django.contrib.auth import get_user_model

from recommend import utils

User = get_user_model()


class Category(models.Model):
    category_name = models.CharField(max_length=10)
    function1 = models.CharField(max_length=10, null=True)
    function2 = models.CharField(max_length=10, null=True)
    function3 = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name

    class Meta:
        ordering = ['-created_at']


class Image(models.Model):
    img_no = models.AutoField(primary_key=True)
    img_path = models.ImageField(upload_to=utils.user_directory_path)
    user_no = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default="유저 정보 없음")


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
    prod_no = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prod_images')
    prod_img_no = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class ProductTag(models.Model):
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prod_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag.tag_text

    class Meta:
        ordering = ['-created_at']


class Review(models.Model):
    review_no = models.AutoField(primary_key=True)
    user_no = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default="유저 정보 없음")
    prod_no = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    review_title = models.CharField(max_length=50, null=True)
    review_text = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    func1_rate = models.CharField(
        ("function1 rate"),
        max_length=1,
        choices=(
            ("g", "Good"),
            ("s", "So so"),
            ("b", "Bad"),
        ),
        default="s"
    )
    func2_rate = models.CharField(
        ("function2 rate"),
        max_length=1,
        choices=(
            ("g", "Good"),
            ("s", "So so"),
            ("b", "Bad"),
        ),
        default="s"
    )
    func3_rate = models.CharField(
        ("function3 rate"),
        max_length=1,
        choices=(
            ("g", "Good"),
            ("s", "So so"),
            ("b", "Bad"),
        ),
        default="s"
    )

    class Meta:
        ordering = ['-created_at']


class ReviewImage(models.Model):
    review_no = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_images')
    review_img_no = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)
    review_is_thumbnail = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class ReviewTag(models.Model):
    review_no = models.ForeignKey(Review, on_delete=models.CASCADE)
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
