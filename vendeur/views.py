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

	prod_list=Product.products()
	return render(request,'main_pages/produits.html',{'prod_list':prod_list,'user':user})

def stat(request):
	user = check_in(request)
	if  user == None:
		return redirect('home')
	return render(request,'main_pages/stat.html',{'user':user})

def action(request):
	user = check_in(request)
	if  user == None:
		return redirect('home')
	return render(request,'main_pages/action.html',{'user':user})
def vendre(request):
	user = check_in(request)
	if  user == None:
		return redirect('home')

	prod_list=Product.products()

	if request.method=="POST":
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

		a=history.objects.filter(hist_date=datetime.date.today(),hist_prod_id_id=prod_id,hist_prix_sell=h_p_s,hist_etat=int(etat))
		if not a.exists():
			history.objects.create(hist_date=datetime.date.today(),hist_nbr_sell=int(qte),hist_money=price*int(qte),hist_prod_id=prod,hist_prix_sell=h_p_s,hist_etat=int(etat))
			history.objects.filter(hist_date=datetime.date.today(),hist_prod_id_id=0).delete()
		else:
			b=a[0]
			b.hist_nbr_sell = b.hist_nbr_sell + int(qte)
			b.hist_money += int(qte)*price
			b.save()

		user.vend_sells=user.vend_sells+int(qte)
		user.vend_money=user.vend_money+price*int(qte)
		user.save()

		prod.prod_Q=prod.prod_Q-int(qte)
		prod.prod_sell=prod.prod_sell+int(qte)
		prod.save()

		return redirect('action')

	return render(request,'main_pages/vendre.html',{'prod_list':prod_list,'user':user})

def stock(request):
	user = check_in(request)
	if  user == None:
		return redirect('home')

	prod_list=Product.products()

	if request.method == "POST":
		prod_id=request.POST.get('prod_id')
		qte=request.POST.get('qte')

		prod= Product.objects.get(id=int(prod_id))
		prod.prod_Q+=int(qte)
		prod.save()
		return redirect('action')
	return render(request,'main_pages/stock.html',{'prod_list':prod_list,'user':user})

def testeur_in(request):
	user = check_in(request)
	if  user == None:
		return redirect('home')

	prod_list=Product.products()

	if request.method == "POST":
		prod_id=request.POST.get('prod_id')
		qte=request.POST.get('qte')
		prod= Product.objects.get(id=int(prod_id))
		prod_test.objects.create(prod=prod,date=datetime.date.today(),qte=int(qte))
		prod.prod_Q-=int(qte)
		prod.save()
		return redirect('action')
	return render(request,'main_pages/testeur.html',{'prod_list':prod_list,'user':user})


def home(request):
	a=history.objects.filter(hist_date=datetime.date.today())
	if(not a.exists()):
		history.objects.create(hist_date=datetime.date.today(),hist_nbr_sell=0,hist_money=0,hist_prod_id=Product.objects.get(id=0),hist_prix_sell=None,hist_etat=1)

	if request.method == "POST":
		form=Connect(request.POST)
		if form.is_valid():
			try:
				user=vendeur.objects.get(vend_user_name=form.cleaned_data['user_name'],vend_code=form.cleaned_data['password'])				
			except:
				user=None
			if user != None:
				hashes=Hash.generate_id(user)
				user_bis.objects.create(user=user,user_coockie_hash= hashes['hashed2'])
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
	prod_list=Product.products()
	return render(request,'main_pages/home.html',{'form':form,'prod_list':prod_list})

def deconncter(request):
	if 'remember_me' in request.COOKIES:
		user_bis.objects.filter(user_coockie_hash=Hash.get_id(request.COOKIES['remember_me'])).delete()

	response= redirect('home')
	response.delete_cookie('check_in')
	response.delete_cookie('remember_me')
	return response

def administration(request):
	user = check_in(request)
	if  user == None or user.vend_admin == 0:
		return HttpResponse('Acces Refusé !!')

	employes=vendeur.vendeurs()
	products=Product.products()
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

		hist_list=history.history_query(date_deb,date_fin)

	return JsonResponse({'hist_list':hist_list,'date_deb':date_deb,'date_fin':date_fin})

def stat_employe_list(request):
	user = check_in(request)
	if  user == None:
		return HttpResponse('Error')
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
			for statis in history.objects.raw("select id,hist_date ,hist_prod_id_id,sum(hist_nbr_sell) as nbr from vendeur_history where hist_date >= '"+str(date_deb)+"' and hist_date <= '"+str(date_fin)+"' and hist_prod_id_id ="+str(prod.id)+" group by hist_date ORDER BY hist_date  asc"):
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
	testeurList=prod_test.tests()
	return JsonResponse({'testeurList':testeurList})


############################" PRINT"
def print_stat(request):
	user = check_in(request)
	if  user == None:
		return HttpResponse('Error')
	return render(request,'print_files/stat.html')

