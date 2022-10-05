from django.contrib.auth.models import User
from django.db import models

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    slug = models.CharField(max_length=150 , null=False , blank=False)
    image = models.ImageField(upload_to='images/category' , null=True , blank=True)
    description = models.TextField(max_length=500 , null=False , blank=False)
    status = models.BooleanField(default=False)
    trending = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=150 , null=False , blank=False)
    meta_keywords = models.CharField(max_length=150 , null=False , blank=False)
    meta_description = models.CharField(max_length=150 , null=False , blank=False)
    parent = models.ForeignKey('Category' , on_delete=models.CASCADE , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    class tag_product(models.TextChoices):
        trending = 'Trending' , 'Trending'
        new = 'NEW' , 'New'
        bestseller = 'Bestseller' , 'Bestseller'
    category = models.ManyToManyField(Category)
    name = models.CharField(max_length=150, null=False, blank=False)
    slug = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to='images/product', null=True, blank=True)
    quantity = models.IntegerField(null=False , blank=False)
    original_price = models.DecimalField(max_digits=8 , decimal_places=2)
    selling_price = models.DecimalField(max_digits=8 , decimal_places=2)
    main_description = models.TextField(max_length=500, null=False, blank=False)
    small_description = models.CharField(max_length=250, null=False, blank=False)
    status = models.BooleanField(default=False)
    tag = models.CharField(max_length=200,choices= tag_product.choices , null=True , blank=True)
    meta_title = models.CharField(max_length=150, null=False, blank=False)
    meta_keywords = models.CharField(max_length=150, null=False, blank=False)
    meta_description = models.CharField(max_length=150, null=False, blank=False)
    additional_information = models.TextField(null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Slider(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='images/slider' , null=False , blank=False)
    status = models.BooleanField(default=False)

class ProductImageGallery(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/gallery')
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product)



class ProductView(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    user_ip = models.CharField(max_length=70)
    user = models.ForeignKey(User , on_delete=models.CASCADE , null=True , blank=True)

    def __str__(self):
        return str(self.product.name)


class Comments(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)