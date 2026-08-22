from django.db import models
from category.models import Category


class Product(models.Model):
    product_name  = models.CharField(max_length=200,unique=True)
    slug          = models.SlugField(max_length=200,unique=True)
    description   = models.TextField(max_length=5000,blank=True)
    discount_price  = models.IntegerField(null=True, blank=True)
    original_price  = models.IntegerField(null=True, blank=True)
    stock         = models.IntegerField()
    is_available  = models.BooleanField(default=True)
    category      = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date  = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    reviews = models.FloatField(default=0.0 , blank=True , null=True)

    def __str__(self):
        return self.product_name

    def discount_percent(self):
        return ((self.original_price - self.discount_price) / self.original_price) * 100

class ProductDetails(models.Model):
    product = models.ForeignKey(Product,related_name='details_image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/products')
    colors = models.CharField(max_length=50 , null=True , blank=True)

class Contact(models.Model):
    name = models.CharField(max_length=200,unique=True) 
    description   = models.TextField(max_length=500,blank=True)
    contact        = models.IntegerField()
    email = models.EmailField()



class CartItem(models.Model):
    product =  models.ForeignKey(Product,on_delete=models.CASCADE) #which product to display
    user=  models.ForeignKey('accounts.Register',on_delete=models.CASCADE)  #which user cart to display
    quantity = models.PositiveIntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        if self.product.discount_price>0:
            return self.product.discount_price * self.quantity

        return self.product.original_price * self.quantity    

    def discount_price(self):
        if self.product.discount_price>0: 
            return (self.product.original_price-self.product.discount_price)*self.quantity
        return 0        

    def __str__(self):
        return self.product.product_name
    


class Wishlist(models.Model):
    product =  models.ForeignKey(Product,on_delete=models.CASCADE) #which product to display
    user=  models.ForeignKey('accounts.Register',on_delete=models.CASCADE)  #which user cart to display
    added_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product.product_name

     
