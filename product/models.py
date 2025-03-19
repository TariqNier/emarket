from django.db import models
from django.contrib.auth.models import User 




class Category(models.TextChoices):
    Computers = 'Computers'
    Food = 'Food'
    Kids = 'Kids'
    Utilites = 'Utilites'
    Home = 'Home'
    
    



class Product(models.Model):
    name = models.CharField(max_length=100,default="",blank=False)
    desc = models.TextField(max_length=100,default="",blank=False,verbose_name="Description")
    price = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    brand = models.CharField(max_length=200,default="",blank=False)
    category = models.CharField(max_length=200,choices=Category.choices,blank=False)
    ratings = models.DecimalField(max_digits=3,decimal_places=2,default=0)
    stock = models.IntegerField(default=0)
    createAt=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.name
    
    
    # class Meta:
    #     verbose_name="order" 
    
#models.py
class Review(models.Model):
    product = models.ForeignKey(Product,null=True,on_delete=models.CASCADE,related_name='reviews')
    user=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    rating = models.IntegerField(default=0)
    comment= models.TextField(max_length=1000,default="",blank=False)
    createAt=models.DateTimeField(auto_now_add=True)
    
   
    
