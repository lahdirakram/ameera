from django.urls import re_path
from django.urls import include
from . import views
urlpatterns = [
	re_path(r'produit/$', views.produit, name="produit"),
	re_path(r'stat/$', views.stat, name="stat"),
	re_path(r'vendre/$', views.vendre, name="vendre"),
	re_path(r'stock/$', views.stock, name="stock"),
	re_path(r'administration/$', views.administration, name="administration"),

	re_path(r'deconncter/$', views.deconncter, name="deconncter"),
	

	re_path(r'update_hist/$', views.update_hist, name="update_history"),
	re_path(r'stat_prod_list/$', views.stat_prod_list, name="stat_prod_list"),
	re_path(r'stat_hist_list/$', views.stat_hist_list, name="stat_hist_list"),
	re_path(r'stat_employe_list/$', views.stat_employe_list, name="stat_employe_list"),
	re_path(r'stat_ventes_non_paye/$', views.stat_ventes_non_paye, name="stat_ventes_non_paye"),
	re_path(r'stat_graph/$', views.stat_graph, name="stat_graph"),
	re_path(r'stat_testeur/$',views.stat_testeur,name="stat_testeur" ),

	re_path(r'stat/print$', views.print_stat, name="print_stat"),

	re_path(r'^$', views.home, name="home"),

]