from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
       
class Type_of_Product(models.Model):
	name=models.CharField(max_length=50)
	
	def __str__(self):
		return self.name
        	
class Users(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	manager=models.BooleanField(default=False)
	
	def __str__(self):
		return self.user.username
	
@receiver(post_save, sender=User)
def create_user_users(sender, instance, created, **kwargs):
    if created:
        Users.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_users(sender, instance, **kwargs):
    instance.users.save()

		
class Product(models.Model):
	name=models.CharField(max_length=50)
	price=models.DecimalField(max_digits=6, decimal_places=2)
	manager_id=models.ForeignKey(Users, on_delete=models.CASCADE)
	category=models.ForeignKey(Type_of_Product, on_delete=models.PROTECT)	
	def __str__(self):
		return self.name
        
class Cart(models.Model):
	quantity=models.IntegerField()
	boughtPrice=models.DecimalField(max_digits=6, decimal_places=2)
	status=models.BooleanField(default=False)
	product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
	users_id=models.ForeignKey(Users,on_delete=models.CASCADE)

	def __str__(self):
		return str(self.product_id)	

class Inventory(models.Model):
	product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
	quantity=models.IntegerField()

	def __str__(self):
		return str(self.product_id)	
