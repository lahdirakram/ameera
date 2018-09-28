from django.db import models

# Create your models here.
class Product(models.Model):
	
	prod_name=models.TextField()
	prod_image=models.FileField(upload_to='images/')
	prod_PU=models.IntegerField(null=True)
	prod_Q=models.IntegerField(null=True)
	prod_sell=models.IntegerField(null=True)


	def __str__(self):
		return self.prod_name	
class history(models.Model):
	
	hist_date=models.DateField()
	hist_prod_id=models.ForeignKey(Product,on_delete=models.CASCADE,null=False)
	hist_nbr_sell=models.IntegerField()
	hist_money=models.BigIntegerField()
	hist_prix_sell=models.IntegerField(null=True)
	hist_etat=models.IntegerField(default=0)

	def __str__(self):
		return self.hist_date.strftime("%B %d, %Y")

class vendeur(models.Model):

	vend_user_name=models.CharField(max_length=100,default="test")
	vend_name=models.TextField()
	vend_code=models.TextField()

	vend_sells=models.IntegerField(default=0)
	vend_abs=models.IntegerField(default=0)
	vend_money=models.IntegerField(default=0)

	vend_admin=models.IntegerField(default=0)

	def __str__(self):
		return self.vend_name

class test(models.Model):

	aa=models.TextField()

class user_bis(models.Model):
	
	user=models.ForeignKey(vendeur,on_delete=models.CASCADE,null=False)
	user_coockie_hash=models.TextField(default="")
		
		
		


