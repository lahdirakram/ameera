from django.shortcuts import render,redirect
from vendeur.models import Product,history,vendeur,user_bis,prod_test
from django.http import HttpResponse
import datetime
from django.http import JsonResponse
from dateutil.relativedelta import relativedelta
from .forms import ProdForm,Connect
import locale
from .functions import Hash

# Create your views here.
locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')

def produit(request):
	user = check_in(request)
	if  user == None:
		return redirect('home')

	prod_list=[]
	for prod in Product.objects.raw("select * from vendeur_product where id > 0"):
		prod_one={'id':prod.id,'name':prod.prod_name,'image':prod.prod_image.url,'pu':prod.prod_PU,'qte':prod.prod_Q,'sell':prod.prod_sell}
		prod_list.append(prod_one)

	saved=''

	if request.method == 'POST':
		form = ProdForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			saved='true'

	return render(request,'main_pages/produits.html',{'prod_list':prod_list,'saved':saved,'user':user})

def stat(request):
	user = check_in(request)
	if  user == None:
		return redirect('home')
	return render(request,'main_pages/stat.html',{'user':user})

def vendre(request):
	user = check_in(request)
	if  user == None:
		return redirect('home')

	prod_list=[]
	for prod in Product.objects.raw("select * from vendeur_product"):
		prod_one={'id':prod.id,'name':prod.prod_name,'image':prod.prod_image,'pu':prod.prod_PU,'qte':prod.prod_Q,'sell':prod.prod_sell}
		prod_list.append(prod_one)

	if request.method=="POST":
		vendeur_id=request.POST.get('vendeur_id')
		prod_id=request.POST.get('prod_id')
		qte=request.POST.get('qte')
		pu=request.POST.get('pu')
		etat=request.POST.get('etat')
		prod= Product.objects.get(id=int(prod_id))

		if pu == '':
			h_p_s=None
			price=prod.prod_PU
		else:
			h_p_s=prod.prod_PU-int(pu)
			price=int(pu)
		try:
			vend =vendeur.objects.get(vend_code=vendeur_id)
		except:
			vend=None

		if vend != None:
			a=history.objects.filter(hist_date=datetime.date.today(),hist_prod_id_id=prod_id,hist_prix_sell=h_p_s,hist_etat=int(etat))
			if not a.exists():
				history.objects.create(hist_date=datetime.date.today(),hist_nbr_sell=int(qte),hist_money=price*int(qte),hist_prod_id=prod,hist_prix_sell=h_p_s,hist_etat=int(etat))
				history.objects.filter(hist_date=datetime.date.today(),hist_prod_id_id=0).delete()
			else:
				b=a[0]
				b.hist_nbr_sell =b.hist_nbr_sell + int(qte)
				b.hist_money += int(qte)*price
				b.save()

			vend.vend_sells=vend.vend_sells+int(qte)
			vend.vend_money=vend.vend_money+price*int(qte)
			vend.save()

			prod.prod_Q=prod.prod_Q-int(qte)
			prod.prod_sell=prod.prod_sell+int(qte)
			prod.save()
		else:
			print('vend error :'+vendeur_id)


	return render(request,'main_pages/vendre.html',{'prod_list':prod_list,'user':user})

def stock(request):
	user = check_in(request)
	if  user == None:
		return redirect('home')

	prod_list=[]
	for prod in Product.objects.raw("select * from vendeur_product"):
		prod_one={'id':prod.id,'name':prod.prod_name,'image':prod.prod_image,'pu':prod.prod_PU,'qte':prod.prod_Q,'sell':prod.prod_sell}
		prod_list.append(prod_one)

	if request.method == "POST":
		vendeur_id=request.POST.get('vendeur_id')
		prod_id=request.POST.get('prod_id')
		qte=request.POST.get('qte')
		if vendeur.objects.filter(vend_code=vendeur_id).exists():
			prod= Product.objects.get(id=int(prod_id))
			prod.prod_Q+=int(qte)
			prod.save()
		else:
			print('vend error :'+vendeur_id)

	return render(request,'main_pages/stock.html',{'prod_list':prod_list,'user':user})
def home(request):

	if request.method == "POST":
		form=Connect(request.POST)
		if form.is_valid():
			a=vendeur.objects.filter(vend_name=form.cleaned_data['user_name'],vend_code=form.cleaned_data['password'])
			b=vendeur.objects.filter(vend_user_name=form.cleaned_data['user_name'],vend_code=form.cleaned_data['password'])

			if a.exists():
				c=a[0]
			else:
				if b.exists():
					c=b[0]
				else:
					c=None

			if c != None:
				hashes=Hash.generate_id(c)
				user_bis.objects.create(user=c,user_coockie_hash= hashes['hashed2'])
				response= redirect('produit')
				response.set_cookie('remember_me',hashes['hashed'],max_age=3600*24*10)
				return response
			else:
				form.add_error(None,'Nom d\'utilisateur ou mot de passe erroné')
	else:
		form=Connect()
		if 'remember_me' in request.COOKIES:
			a=user_bis.objects.filter(user_coockie_hash=Hash.get_id(request.COOKIES['remember_me']))
			if a.exists():
				return redirect('produit')
	return render(request,'main_pages/home.html',{'form':form})

def deconncter(request):
	if 'remember_me' in request.COOKIES:
		user_bis.objects.filter(user_coockie_hash=Hash.get_id(request.COOKIES['remember_me'])).delete()

	response= redirect('home')
	response.delete_cookie('check_in')
	response.delete_cookie('remember_me')
	return response

def administration(request):
	user = check_in(request)
	if  user == None:
		return HttpResponse('')
	if user.vend_admin == 0:
		return HttpResponse('')

	employes=[]
	products=[]

	for p in Product.objects.all():
		if p.id != 0:
			prod={'code':p.id,'nom':p.prod_name,'image':p.prod_image.url,'qte':p.prod_Q,'sell':p.prod_sell,'prix':p.prod_PU}
			products.append(prod)

	for e in vendeur.objects.all():
		emp={'id':e.id,'nom':e.vend_name,'username':e.vend_user_name,'type':e.vend_admin}
		employes.append(emp)




	return render(request,'main_pages/administration.html',{'employes':employes,'products':products,'user':user})






######################################### background views #########

def update_hist(request):
	res='notdone'
	user = check_in(request)
	if  user == None:
		return HttpResponse(res)
	if request.method == "POST":
		hist=history.objects.get(id=int(request.POST.get('hist_id')))
		hist.hist_etat=1
		hist.save()
		res='done'
	return HttpResponse(res)

def check_in(request):
	if 'remember_me' in request.COOKIES:
		a=user_bis.objects.filter(user_coockie_hash=Hash.get_id(request.COOKIES['remember_me']))
		if a.exists():
			user_coockie=a[0]
			return a[0].user
	return None

def stat_prod_list(request):

	user = check_in(request)
	if  user == None:
		return HttpResponse('Error')

	print_=None

	if request.method == "POST":
		prod_list=[]
		for prod in Product.objects.raw("select p.id,p.prod_name,p.prod_Q,p.prod_sell,sum(h.hist_money) total from vendeur_product p,vendeur_history h where p.id=h.hist_prod_id_id and p.id>0 and h.hist_etat = 1 group by h.hist_prod_id_id"):
			prod_one={'id':prod.id,'name':prod.prod_name,'qte':prod.prod_Q,'sell':prod.prod_sell,'total':prod.total,'credit': 0}
			prod_list.append(prod_one)
		for prod in Product.objects.raw("select p.id,sum(h.hist_money) credit from vendeur_product p,vendeur_history h where p.id=h.hist_prod_id_id and p.id>0 and h.hist_etat = 0 group by h.hist_prod_id_id"):
			prod_list[prod.id-1]['credit']=prod.credit
		if request.POST.get('print') == 'true':
			print_ = 'some thing';

	return render(request,'parts_of_pages/stat_prod_list.html',{'prod_list':prod_list,'print':print_})

def stat_hist_list(request):
	user = check_in(request)
	if  user == None:
		return HttpResponse('Error')
	hist_list=[]
	date_deb=datetime.date.today().replace(day=1)
	date_fin=date_deb + relativedelta(months=1) - relativedelta(day=1)
	if request.method=="POST":
		if request.POST.get('date_debut') is not None:
			date_deb=request.POST.get('date_debut')
		if request.POST.get('date_fin') is not None:
			date_fin=request.POST.get('date_fin')

		for hist in history.objects.raw('select * from vendeur_history where hist_date >= "'+str(date_deb)+'" and hist_date < "'+str(date_fin)+'" ORDER BY hist_date desc'):
			hist_one={'date':hist.hist_date.strftime('%d %B %Y'),'prod':hist.hist_prod_id.prod_name,'qte':hist.hist_nbr_sell,'pred':hist.hist_prix_sell,'money':hist.hist_money,'etat':hist.hist_etat}
			hist_list.append(hist_one)

	return JsonResponse({'hist_list':hist_list,'date_deb':date_deb,'date_fin':date_fin})

def stat_employe_list(request):
	user = check_in(request)
	if  user == None:
		return HttpResponse('Error')

	emp_list=[]
	if request.method=="POST":
		emp_list=vendeur.objects.all()

	return render(request,'parts_of_pages/stat_employe_list.html',{'emp_list':emp_list})
def stat_ventes_non_paye(request):
	user = check_in(request)
	if  user == None:
		return HttpResponse('Error')

	v_n_p=[]
	print_=None
	if request.method=="POST":
		v_n_p=history.objects.filter(hist_etat=0)
		if request.POST.get('print') == 'true':
			print_ = 'some thing';
	return render(request,'parts_of_pages/stat_ventes_non_paye.html',{'v_n_p':v_n_p,'print':print_})

def stat_graph(request):
	user = check_in(request)
	if  user == None:
		return redirect('home')

	ventes_graph_series=[]
	money_graph_series=[]

	sell_list=[]
	money_list=[]

	date_deb=datetime.date.today().replace(day=1)
	date_fin=date_deb + relativedelta(months=1) - relativedelta(day=1)

	if request.method=="POST":
		if request.POST.get('date_debut') is not None:
			date_deb=request.POST.get('date_debut')
		if request.POST.get('date_fin') is not None:
			date_fin=request.POST.get('date_fin')

	for prod in Product.objects.all():
		if prod.id != 0:
			prod_obj={'name':prod.prod_name,'data':[]}
			sell_list=[]
			for statis in history.objects.raw("select id,hist_date ,hist_prod_id_id,hist_nbr_sell as nbr from vendeur_history where hist_date >= '"+str(date_deb)+"' and hist_date <= '"+str(date_fin)+"' and hist_prod_id_id ="+str(prod.id)+" ORDER BY hist_prod_id_id,hist_date  asc"):
				sell_one=[[statis.hist_date.strftime("%d"),statis.hist_date.strftime("%m"),statis.hist_date.strftime("%y")],statis.nbr]
				sell_list.append(sell_one)
			prod_obj['data']=sell_list
			ventes_graph_series.append(prod_obj)

	for statis in history.objects.raw("select id,hist_date,sum(hist_money) as money from vendeur_history where hist_date >= '"+str(date_deb)+"' and hist_date <= '"+str(date_fin)+"'  group by hist_date order by hist_date asc"):
		money_one=[[int(statis.hist_date.strftime("%d")),int(statis.hist_date.strftime("%m")),int("20"+statis.hist_date.strftime("%y"))],statis.money]
		money_list.append(money_one)
	money_graph_series=[{'name': 'Money','data': money_list }]
	return JsonResponse({'money_graph_series':money_graph_series,'ventes_graph_series':ventes_graph_series,'d_d':str(date_deb),'d_f':str(date_fin)})
def stat_testeur(request):
	
	user = check_in(request)
	if  user == None:
		return HttpResponse('Acces non autorisé')

	testeurList=[]
	if request.method == "POST":
		for testeur in prod_test.objects.all():
			test = {'date':testeur.date,'prod':testeur.prod.prod_name,'qte':testeur.qte}
			testeurList.append(test)

	return JsonResponse({'testeurList':testeurList})
		

############################" PRINT"
def print_stat(request):
	user = check_in(request)
	if  user == None:
		return HttpResponse('Error')
	return render(request,'print_files/stat.html')