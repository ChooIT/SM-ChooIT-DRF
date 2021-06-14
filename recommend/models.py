from django.db import models

from accounts.models import Tag


class Product(models.Model):
    prod_no = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=100, null=False)
    prod_manufacturer = models.CharField(max_length=30)
    prod_price = models.CharField(max_length=10, null=False)
    prod_func1 = models.CharField(max_length=10)
    prod_func2 = models.CharField(max_length=10)
    prod_func3 = models.CharField(max_length=10)
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
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
