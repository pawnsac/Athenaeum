from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('search/', views.search, name="search"),
	path('viewb/', views.view_book, name="view_book"),
	path('catalog/', views.catalog, name="catalog"),
	path('login/', views.login, name="login"),
	path('atc/', views.atc, name="atc"),
	path('main_redirect/', views.main_redirect, name="main_redirect"),
	path('dbook/', views.dbook, name="dbook"),
	path('w_store/', views.w_store, name="w_store"),
	path('add_book/', views.add_book, name="add_book"),
	path('abr/', views.abr, name="abr"),
	path('w_catalog/', views.w_catalog, name="w_catalog"),
	path('w_vbook/', views.w_vbook, name="w_vbook"),
	path('w_main_redirect/', views.w_main_redirect, name="w_main_redirect"),
	path('w_search/', views.w_search, name="w_search"),
	path('viewbf/', views.view_bookf, name="view_bookf"),
	path('register/', views.register, name="register"),
	path('update_profile/', views.update_profile, name="update_profile"),
	path('search_genre/', views.search_genre, name="search_genre"),
	path('addreview/', views.addreview, name="addreview"),
	path('manual/', views.manual, name="manual"),
	path('w_manual/', views.w_manual, name="w_manual"),


]