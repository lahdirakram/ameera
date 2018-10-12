from django.db import models

# Create your models here.
class Product(models.Model):
	
	prod_name=models.TextField()
	prod_image=models.FileField(upload_to='images/')
	prod_PU=models.IntegerField(null=True)
	prod_Q=models.IntegerField(null=True)
	prod_sell=models.IntegerField(null=True)

	@staticmethod
	def products():
		products=[]
		for p in Product.objects.all():
			if p.id != 0:
				prod={'id':p.id,'name':p.prod_name,'image':p.prod_image.url,'qte':p.prod_Q,'sell':p.prod_sell,'pu':p.prod_PU}
				products.append(prod)
		return products;

	def __str__(self):
		return self.prod_name	
class history(models.Model):
	
	hist_date=models.DateField()
	hist_prod_id=models.ForeignKey(Product,on_delete=models.CASCADE,null=False)
	hist_nbr_sell=models.IntegerField()
	hist_money=models.BigIntegerField()
	hist_prix_sell=models.IntegerField(null=True)
	hist_etat=models.IntegerField(default=0)

	@staticmethod
	def history_query(date_deb,date_fin):
		hist_list=[]
		for hist in history.objects.raw('select * from vendeur_history where hist_date >= "'+str(date_deb)+'" and hist_date < "'+str(date_fin)+'" ORDER BY hist_date desc'):
			hist_one={'date':hist.hist_date.strftime('%d %B %Y'),'prod':hist.hist_prod_id.prod_name,'qte':hist.hist_nbr_sell,'pred':hist.hist_prix_sell,'money':hist.hist_money,'etat':hist.hist_etat}
			hist_list.append(hist_one)
		return hist_list

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

	@staticmethod
	def vendeurs():
		employes=[]
		for e in vendeur.objects.all():
			emp={'id':e.id,'nom':e.vend_name,'username':e.vend_user_name,'type':e.vend_admin}
			employes.append(emp)
		return employes;

	def __str__(self):
		return self.vend_name

class user_bis(models.Model):
	
	user=models.ForeignKey(vendeur,on_delete=models.CASCADE,null=False)
	user_coockie_hash=models.TextField(default="")

class prod_test(models.Model):
	
	prod=models.ForeignKey(Product,on_delete=models.CASCADE,null=False)
	date=models.DateField()
	qte=models.IntegerField(default=1)

	@staticmethod
	def tests():
		testeurList=[]
		for t in prod_test.objects.all():
			test = {'date':t.date.strftime('%d %B %Y'),'prod':t.prod.prod_name,'qte':t.qte}
			testeurList.append(test)
		return testeurList
		
	def __str__(self):
		return self.prod.prod_name
		
		
		


