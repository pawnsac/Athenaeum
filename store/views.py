from django.shortcuts import render
from django.shortcuts import redirect
from .models import * 
from django import forms
from .forms import SearchForm
import json
import datetime
import sqlite3

def store(request, customer=None):
	if(customer==None):
		return redirect('login')
	conn=sqlite3.connect("db.db")
	c=conn.cursor()
	c.execute("SELECT customers_name  FROM customer where customer_id= ?",(customer,))
	name = c.fetchone()[0]
	c.execute("SELECT * FROM shopping_cart where customer_id= ?",(customer,))
	sc=c.fetchall()
	citems=len(sc)
	c.close()
	context = {'name':name, 'citems':citems, 'customer':customer}
	return render(request, 'store/store.html', context)

def cart(request):
	customer=int(request.POST.get('id', False))
	conn=sqlite3.connect("db.db")
	c=conn.cursor()
	c.execute("SELECT * FROM shopping_cart where customer_id= ?",(customer,))
	boks = c.fetchall()
	books=[]
	print(boks)
	total_price=0
	for book in boks:
		book_id=book[2]
		c.execute("SELECT * FROM books where book_id = ? ",(book_id,))
		b=c.fetchone()
		total_price+=b[10]
		books.append(b)

	c.execute("SELECT * FROM shopping_cart where customer_id= ?",(customer,))
	sc=c.fetchall()
	print(sc)
	citems=len(sc)
	items=books
	context = {'items':items, 'customer':customer,'citems':citems,'total_price':total_price}
	return render(request, 'store/cart.html', context)

def checkout(request):
	conn=sqlite3.connect("db.db")
	customer=int(request.POST.get('id', False))
	c=conn.cursor()
	c.execute("SELECT * FROM shopping_cart where customer_id= ?",(customer,))
	boks = c.fetchall()
	books=[]
	total_price=0
	for book in boks:
		book_id=book[2]
		c.execute("SELECT * FROM books where book_id = ? ",(book_id,))
		b=c.fetchone()
		total_price+=b[10]
		books.append(b)

	c.execute("SELECT * FROM shopping_cart where customer_id= ?",(customer,))
	sc=c.fetchall()
	print(sc)
	citems=len(sc)
	items = []
	order = {'get_cart_total':0, 'get_cart_items':0}
	c=conn.cursor()
	
	print(customer)
	ccn=int(request.POST.get('ccn', False))
	cvc=int(request.POST.get('cvc', False))

	c.execute("SELECT cvc FROM credit_card where credit_card_no= ?",(ccn,))
	og=c.fetchall()
	if(og!=[]):
		if(int(og[0][0])==cvc):
			c.execute("SELECT * FROM shopping_cart where customer_id= ?",(customer,))
			books=c.fetchall()
			for book in books:
				book_id=book[2]	
				c.execute("insert into customers_Catalog values(?,?,?)",(customer,book_id,"1"))
				c.execute("DELETE FROM shopping_cart WHERE book_id=? and customer_id= ?",(book_id,customer,))
			conn.commit()
			return store(request, customer)
		else:
			items = []
			order = {'get_cart_total':0, 'get_cart_items':0}

	context = {'items':items, 'order':order, 'customer':customer,'citems':citems,'total_price':total_price}
	return render(request, 'store/checkout.html', context)

def search(request):
	conn=sqlite3.connect("db.db")
	c=conn.cursor()
	if request.method == 'POST':
        # create a form instance and populate it with data from the request:
		form = SearchForm(request.POST)
        # check whether it's valid:
		if form.is_valid():
			txt= form.cleaned_data
			txt=txt['search_text']
			customer=int(request.POST['id'])
			c.execute("SELECT * FROM books where title like ? ",('%'+txt+'%',))
			books = c.fetchall()
			c.execute("SELECT * FROM shopping_cart where customer_id= ?",(customer,))
			sc=c.fetchall()
			citems=len(sc)
			c.execute("SELECT * FROM customers_Catalog where customer_id= ?",(customer,))
			boks = c.fetchall()
			books_c=[]
			books=[[i for i in book] for book in books]
			for book in boks:
				book_id=book[1]
				c.execute("SELECT * FROM books where book_id = ? ",(book_id,))
				books_c.append(c.fetchone())
			books_c=[[i for i in book] for book in books_c]
			print(books_c)
			for element in books:
				if element in books_c:
					books.remove(element)
			for element in books:
				if element in books_c:
					books.remove(element)
			print(books)
			nobooks=False
			if(books==[]):
				nobooks=True
			context = {'books':books,'customer':customer,'citems':citems,'nobooks':nobooks}	
			return render(request, 'store/search.html', context)
	customer=int(request.POST['id'])
	c.execute("SELECT * FROM shopping_cart where customer_id= ?",(customer,))
	sc=c.fetchall()
	citems=len(sc)
	nobooks=True
	return render(request, 'store/search.html', {'books':[],'customer':customer,'citems':citems,'nobooks':nobooks})
def view_book(request):
	conn=sqlite3.connect("db.db")
	c=conn.cursor()
	customer=int(request.POST.get('id', False))
	c.execute("SELECT * FROM shopping_cart where customer_id= ?",(customer,))
	sc=c.fetchall()
	citems=len(sc)

	if request.method == 'POST':
        # create a form instance and populate it with data from the request:
		txt  = request.POST['book_id']
		txt=int(txt)
		c.execute("SELECT * FROM books where book_id = ? ",(txt,))
		books = c.fetchall()
		c.execute("SELECT * FROM reviews where book_id = ? ",(txt,))
		reviews = c.fetchall()
		reviews=[[i for i in book] for book in reviews]
		count=len(reviews)
		rating=0
		i=0

		if(count!=0):
			for r in reviews:
				c.execute("SELECT customers_name FROM customer where customer_id = ? ",(int(r[3]),))
				name = c.fetchone()[0]
				rating+=r[4]
				reviews[i][2]=name
				i+=1
			rating/=count

		c.close()
		context = {'books':books, 'customer':customer,'citems':citems,'reviews':reviews, 'rating':rating}

		return render(request, 'store/viewb.html', context)

	return render(request, 'store/viewb.html', {'books':[]})


def catalog(request):
	customer=int(request.POST.get('id', False))
	conn=sqlite3.connect("db.db")
	c=conn.cursor()
	c.execute("SELECT * FROM shopping_cart where customer_id= ?",(customer,))
	sc=c.fetchall()
	print(sc)
	citems=len(sc)
	c.execute("SELECT * FROM customers_Catalog where customer_id= ?",(customer,))
	boks = c.fetchall()
	books=[]
	print(boks)
	for book in boks:
		book_id=book[1]
		c.execute("SELECT * FROM books where book_id = ? ",(book_id,))
		books.append(c.fetchone())

	c.close()
	context = {'books':books, 'customer':customer ,'citems':citems}
	return render(request, 'store/catalog.html', context)


def login(request):
	conn=sqlite3.connect("db.db")
	c=conn.cursor()
	a=0
	if a==1:
		x=1
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			
			password =request.POST.get('password')

			c.execute("SELECT password FROM customer where email_adress= ?",(username,))
			passw=c.fetchall()
			c.execute("SELECT password FROM writer where email_adress= ?",(username,))
			passww=c.fetchall()
			print(passw)
			if(passw!=[]):
				passw=passw[0][0]
			if(passww!=[]):
				passww=passww[0][0]
			if(passw==password):
				c.execute("SELECT customer_id FROM customer where email_adress= ?",(username,))
				id=c.fetchone()[0]
				print(id)
				return store(request, id)
			elif passww==password:
				c.execute("SELECT writer_id FROM writer where email_adress= ?",(username,))
				id=c.fetchone()[0]
				print(id)
				return w_store(request, id)
			else:
				return redirect('login')

		context = {}
		return render(request, 'store/login.html', context)
def atc(request):
	conn=sqlite3.connect("db.db")
	c=conn.cursor()
	if request.method == 'POST':
		txt  = request.POST['book_id']
		cid=int(request.POST['id'])
		txt=int(txt)
		c.execute("SELECT * FROM books where book_id = ? ",(txt,))
		books = c.fetchone()

		c.execute("insert into shopping_cart values(?,?,?,?,?)",(cid,cid,txt,books[10],datetime.datetime.now()))
		conn.commit()
		conn.close()
		return store(request, cid)

	return render(request, 'store/viewb.html', {'books':[]})

def main_redirect(request):
	customer=int(request.POST.get('id', False))
	return store(request, customer)

def dbook(request):
	conn=sqlite3.connect("db.db")
	c=conn.cursor()
	customer=int(request.POST.get('id', False))
	book_id  = int(request.POST.get('book_id', False))
	print(book_id)
	c.execute("DELETE FROM shopping_cart WHERE book_id=? and customer_id= ?",(book_id,customer,))
	conn.commit()

	return cart(request)



def w_store(request,writer=None):
	if(writer==None):
		return redirect('login')
	conn=sqlite3.connect("db.db")
	c=conn.cursor()
	c.execute("SELECT writer_name  FROM writer where writer_id= ?",(writer,))
	name = c.fetchone()[0]
	context = { 'writer':writer,'name':name}
	return render(request, 'store/writer/store.html', context)
def w_main_redirect(request):
	writer=int(request.POST.get('id', False))
	return w_store(request, writer)


def add_book(request):
	writer=request.POST.get('writer')
	context = { 'writer':writer}
	return render(request, 'store/writer/add_book.html', context)


def abr(request):
	writer=request.POST.get('id')
	context = { 'writer':writer}
	return render(request, 'store/writer/add_book.html', context)
def add_book(request):
	conn=sqlite3.connect("db.db")
	c=conn.cursor()
	writer=request.POST.get('id')
	if request.method == 'POST':
		title=request.POST.get('title')
		Price=request.POST.get('price')
		isbn=request.POST.get('isbn')
		genre=request.POST.get('genre')
		summary=request.POST.get('summary')
		language=request.POST.get('language')
		title=request.POST.get('title')
		num_pages=request.POST.get('pages')
		book_text=""""""
		book_text+=request.POST.get('text')
		reviews_count=0
		average_rating=0
		writer_id=int(writer)
		publishing_id="1"
		c.execute("select writer_name from writer where writer_id=?",(writer,))
		writer_name=c.fetchall()
		writer_name=writer_name[0][0]
		print(writer_name)
		try:
			c.execute("insert into books(title,writer_name, writer_id,isbn,language,num_pages,reviews_count,average_rating,genre,Price,summary,book_text,publishing_id) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",(title,writer_name, writer_id,isbn,language,num_pages,reviews_count,average_rating,genre,Price,summary,book_text,publishing_id,))
			c.execute("select book_id from books where num_pages=? and writer_id=? and isbn=?",(num_pages,writer_id,isbn,))
			book_id=c.fetchone()[0]
			c.execute("insert into writers_catalog values(?,?,?)",(writer_id,book_id,"OOF"))
			conn.commit()
			context = { 'writer':writer}
			return w_store(request,writer)
		except:
			context = { 'writer':writer}
			return render(request, 'store/writer/add_book.html', context)

def w_catalog(request):
	writer=int(request.POST.get('id', False))
	conn=sqlite3.connect("db.db")
	c=conn.cursor()
	c.execute("SELECT * FROM writers_catalog where writer_id= ?",(writer,))
	boks = c.fetchall()
	books=[]
	print(boks)
	for book in boks:
		book_id=book[1]
		c.execute("SELECT * FROM books where book_id = ? ",(book_id,))
		books.append(c.fetchone())
	c.close()
	context = {'books':books, 'writer':writer }
	return render(request, 'store/writer/catalog.html', context)

def w_vbook(request):
	conn=sqlite3.connect("db.db")
	c=conn.cursor()
	writer=int(request.POST.get('id', False))
	if request.method == 'POST':
        # create a form instance and populate it with data from the request:
		txt  = request.POST['book_id']
		txt=int(txt)
		c.execute("SELECT * FROM books where book_id = ? ",(txt,))
		books = c.fetchall()
		c.execute("SELECT * FROM reviews where book_id = ? ",(txt,))
		reviews = c.fetchall()
		reviews=[[i for i in book] for book in reviews]
		count=len(reviews)
		rating=0
		i=0
		if(count!=0):
			for r in reviews:
				
				c.execute("SELECT customers_name FROM customer where customer_id = ? ",(int(r[3]),))
				name = c.fetchone()[0]
				rating+=r[4]
				reviews[i][2]=name
				i+=1
			rating/=count

		c.close()


		context = {'books':books, 'writer':writer,'reviews':reviews, 'rating':rating}	
		return render(request, 'store/writer/viewb.html', context)

	return render(request, 'store/writer/viewb.html', {'books':[],'writer':writer})

def w_search(request):
	conn=sqlite3.connect("db.db")
	c=conn.cursor()
	if request.method == 'POST':
        # create a form instance and populate it with data from the request:
		form = SearchForm(request.POST)
        # check whether it's valid:
		if form.is_valid():
			txt= form.cleaned_data
			txt=txt['search_text']
			writer=int(request.POST['id'])
			c.execute("SELECT * FROM books where title like ? ",('%'+txt+'%',))
			books = c.fetchall()
			nobooks=False
			if(books==[]):
				nobooks=True
			context = {'books':books,'writer':writer,'nobooks':nobooks}	
			return render(request, 'store/writer/search.html', context)
	writer=int(request.POST['id'])
	c.execute("SELECT * FROM shopping_cart where customer_id= ?",(customer,))
	sc=c.fetchall()
	citems=len(sc)
	nobooks=True
	return render(request, 'store/writer/search.html', {'books':[],'writer':writer,'nobooks':nobooks})

def view_bookf(request):
	conn=sqlite3.connect("db.db")
	c=conn.cursor()
	customer=int(request.POST.get('id', False))
	c.execute("SELECT * FROM shopping_cart where customer_id= ?",(customer,))
	sc=c.fetchall()
	citems=len(sc)

	if request.method == 'POST':
        # create a form instance and populate it with data from the request:
		txt  = request.POST['book_id']
		txt=int(txt)
		c.execute("SELECT * FROM books where book_id = ? ",(txt,))
		books = c.fetchall()
		c.close()
		context = {'books':books, 'customer':customer,'citems':citems}	
		return render(request, 'store/viewbf.html', context)

	return render(request, 'store/viewbf.html', {'books':[]})

def register(request):
	conn=sqlite3.connect("db.db")
	c=conn.cursor()

	if(request.method=='POST'):
		utype=request.POST['utype']
		name=request.POST['name']
		email=request.POST['email']
		password=request.POST['password']
		if(utype=="writer"):
			c.execute("insert into writer(writer_name,email_adress,password) values(?,?,?)",(name,email,password))
			conn.commit()
			return redirect('login')
		elif(utype=="customer"):
			c.execute("insert into customer(customers_name,email_adress,password) values(?,?,?)",(name,email,password))
			conn.commit()
			return redirect('login')


		else:
			return redirect('register')
	return render(request, 'store/register.html', {})


def update_profile(request):
	customer=int(request.POST.get('id', False))
	conn=sqlite3.connect("db.db")
	c=conn.cursor()
	c.execute("SELECT * FROM shopping_cart where customer_id= ?",(customer,))
	sc=c.fetchall()
	citems=len(sc)
	context = {'customer':customer,'citems':citems}	
	if request.POST.get('password1', False)!=False:
		p1=request.POST.get('password1', False)
		p2=request.POST.get('password2', False)
		if(p1==p2):
			c.execute("update customer set password=? where customer_id =?",(p1,customer,))
			conn.commit()
			return store(request,customer)
	if request.POST.get('e1', False)!=False:
		p1=request.POST.get('e1', False)
		p2=request.POST.get('e2', False)
		if(p1==p2):
			c.execute("update customer set email_adress=? where customer_id =?",(p1,customer,))
			conn.commit()
			return store(request,customer)
	return render(request,'store/update_profile.html',context)
def search_genre(request):
	conn=sqlite3.connect("db.db")
	c=conn.cursor()
	if request.method == 'POST':
		if request.POST.get('genre', False):
			genre=request.POST.get('genre', False)
			customer=int(request.POST['id'])
			c.execute("SELECT * FROM books where genre = ? ",(genre,))
			books = c.fetchall()
			c.execute("SELECT * FROM shopping_cart where customer_id= ?",(customer,))
			sc=c.fetchall()
			citems=len(sc)
			c.execute("SELECT * FROM customers_Catalog where customer_id= ?",(customer,))
			boks = c.fetchall()
			books_c=[]
			books=[[i for i in book] for book in books]
			for book in boks:
				book_id=book[1]
				c.execute("SELECT * FROM books where book_id = ? ",(book_id,))
				books_c.append(c.fetchone())
			books_c=[[i for i in book] for book in books_c]
			print(books_c)
			for element in books:
				if element in books_c:
					books.remove(element)
			for element in books:
				if element in books_c:
					books.remove(element)
			print(books)
			nobooks=False
			if(books==[]):
				nobooks=True
			context = {'books':books,'customer':customer,'citems':citems,'nobooks':nobooks}	
			return render(request, 'store/search.html', context)
	customer=int(request.POST['id'])
	c.execute("SELECT * FROM shopping_cart where customer_id= ?",(customer,))
	sc=c.fetchall()
	citems=len(sc)
	nobooks=True
	return render(request, 'store/search.html', {'books':[],'customer':customer,'citems':citems,'nobooks':nobooks})


def addreview(request):
	conn=sqlite3.connect("db.db")
	c=conn.cursor()
	customer=int(request.POST['id'])
	c.execute("SELECT * FROM shopping_cart where customer_id= ?",(customer,))
	sc=c.fetchall()
	citems=len(sc)
	book=request.POST.get('book_ids', False)
	if request.POST.get('stars', False)!=False and request.POST.get('description', False)!=False:
		book_id=request.POST.get('book_id', False)
		d=request.POST.get('description', False)
		s=int(request.POST.get('stars', False))
		c.execute("insert into reviews(book_id,customer_id,rating,review_text) values(?,?,?,?)",(book_id,customer,s,d,))
		conn.commit()
		return store(request,customer)
	return render(request, 'store/addreview.html', {'books':[],'customer':customer,'citems':citems,'book':book})

def manual(request):
	conn=sqlite3.connect("db.db")
	c=conn.cursor()
	customer=int(request.POST.get('id', False))
	c.execute("SELECT * FROM shopping_cart where customer_id= ?",(customer,))
	sc=c.fetchall()

	citems=len(sc)
	manual=""" Readers: As a reader you can search, buy and read books online. In order to buy a book search for it using the search bar or explore by genre option -> add the book to your shopping cart -> go to your shopping cart -> proceed to checkout -> confirm payment. The book will be added to your catalog.
"""
	context={'customer':customer,'citems':citems,'manual':manual}

	return render(request, 'store/manual.html', context)

def w_manual(request):
	conn=sqlite3.connect("db.db")
	c=conn.cursor()
	writer=int(request.POST.get('id', False))
	manual="""Writers can sell their books online on Athaneum. To add a book go to add book option, fill in the information and the book will be added to the writer's catalog and will be available for the customers to buy. Writers can also look at their publised books and their reviews by going to the catalog."""
	
	context={'writer':writer,'manual':manual}

	return render(request, 'store/writer/manual.html', context)

