from django.db import models

from accounts.models import Tag
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from recommend import utils

User = get_user_model()


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=10, unique=True)
    function1 = models.CharField(max_length=10, null=True)
    function2 = models.CharField(max_length=10, null=True)
    function3 = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name

    class Meta:
        ordering = ['-created_at']


class Product(models.Model):
    prod_no = models.AutoField(primary_key=True)
    prod_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, default="1")
    prod_name = models.CharField(max_length=100, null=False)
    prod_manufacturer = models.CharField(max_length=30)
    prod_price = models.CharField(max_length=10, null=False)
    prod_preference = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        default=50
    )
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%d. [%s]%s" % (self.prod_no, self.prod_manufacturer, self.prod_name)

    class Meta:
        ordering = ['prod_category_id', 'prod_no']


class ProductImage(models.Model):
    img_no = models.AutoField(primary_key=True)
    prod_no = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prod_images')
    prod_img_path = models.ImageField(upload_to=utils.user_directory_path)
    prod_is_thumbnail = models.BooleanField(default=False)
    user_no = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['prod_no', '-prod_is_thumbnail', 'img_no']


class ProductTag(models.Model):
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prod_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag.tag_text

    class Meta:
        ordering = ['-created_at']


class ReviewImage(models.Model):
    img_no = models.AutoField(primary_key=True)
    img_path = models.ImageField(upload_to=utils.user_directory_path)
    user_no = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Review(models.Model):
    review_no = models.AutoField(primary_key=True)
    user_no = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    prod_no = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_title = models.CharField(max_length=50, null=True)
    review_text = models.TextField(null=True)
    review_img_thumbnail = models.ForeignKey(ReviewImage, on_delete=models.SET_NULL, null=True)
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


class ReviewTag(models.Model):
    review_no = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag.tag_text

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
        unique_together = ['fav_user', 'fav_prod']


class Estimate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    estimate_rate = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ],
        default=3
    )

    class Meta:
        unique_together = ['user', 'prod']


class Option(models.Model):
    option_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=10, null=True)
    category = models.CharField(max_length=10, null=True)
    classification = models.CharField(max_length=10, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "[{%s}] %s" % (self.title, self.tag.tag_text)

    class Meta:
        unique_together = ['title', 'tag']
        ordering = ['title', 'option_id']
