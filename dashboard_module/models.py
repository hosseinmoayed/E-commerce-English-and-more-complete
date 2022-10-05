from django.contrib.auth.models import User
from django.core.validators import MinValueValidator , MaxValueValidator , EmailValidator
from django.db import models

# Create your models here.
from store_module.models import Product


class Cart(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=400,null=True , blank=True)
    Country = models.CharField(max_length=50,null=True , blank=True)
    State = models.CharField(max_length=50,null=True , blank=True)
    zip = models.CharField(max_length=100 , null=True , blank=True)
    Independent_amount = models.IntegerField(null=True , blank=True)
    amount_paid = models.IntegerField(null=True , blank=True)
    payment_date = models.DateTimeField(auto_now=True ,null=True , blank=True)
    transection_id = models.CharField(max_length=200 , null=True , blank=True)

    def __str__(self):
        return str(self.user)

    @property
    def total(self):
        total = 0
        for item in self.item_set.filter(product__status=True):
            total += item.subtotal
        return total

    @property
    def item_count(self):
        return self.item_set.filter(product__status=True).count()


class Item(models.Model):
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    final_price = models.DecimalField(max_digits=8 , decimal_places=2 , null=True , blank=True)

    def __str__(self):
        return str(self.product.name)


    @property
    def subtotal(self):
        return self.quantity * self.product.selling_price

    @property
    def final_subtotal(self):
        return self.quantity * self.final_price

class Discountcodes(models.Model):
    code = models.CharField(max_length=50 , unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    discount = models.IntegerField(validators=[MinValueValidator(0) , MaxValueValidator(100)])
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class UserDiscountCode(models.Model):
    cart = models.OneToOneField(Cart , on_delete=models.CASCADE , null=True)
    code = models.ForeignKey(Discountcodes , on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    def __str__(self):
        return str(self.cart.user)


class UserInfo(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100 , null=True , blank=False)
    lastname = models.CharField(max_length=100 , null=True , blank=False)
    address = models.CharField(max_length=400)
    Country = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    zip = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='images/avatar')

    def __str__(self):
        return str(self.user)



class Comment(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    userinfo = models.ForeignKey(UserInfo , on_delete=models.CASCADE , null=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)






