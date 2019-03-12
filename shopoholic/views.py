from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import sqlite3
import sys
sys.path.insert(0, '../')
from global_util import products_from_db,logged_in,rating_sort_get,review_sort_get


def login(request):
	if request.method == 'POST':
		user_name = request.POST['temp_uname']
		password = request.POST['temp_pass']
		print(user_name, password)
		connect = sqlite3.connect("db.sqlite3")
		c = connect.cursor()
		c.execute('SELECT Password FROM Users WHERE Username = ?', (user_name,))
		row = c.fetchone()
		print(row)
		if row is None:
			print('not_reg')
			return render(request, 'login.html', {'not_reg': True})
		elif password != row[0]:
			print('wrong_pass')
			return render(request, 'login.html', {'bad_cred': True})
		else:
			print('OK')
			# logged_in = True
			prod_dict = products_from_db()
			prod_dict['uname'] = user_name
			# prod_dict['sort'] = True
			response = render(request, 'home.html', prod_dict)
			response.set_cookie('user_name', user_name)
			return response

	return render(request, 'login.html')

def product(request):
	pname = request.GET['pname']
	connect = sqlite3.connect("db.sqlite3")
	c = connect.cursor()
	if request.COOKIES['user_name']: 
		user_name = request.COOKIES['user_name']
		logged_in = True
	if request.method == 'POST':
		rating = request.POST.get('rating', 5)
		review = request.POST['review']
		c.execute("INSERT INTO Reviews VALUES(?,?,?,?)", (user_name,pname,review.lower(),rating,))
		connect.commit()

	c.execute('SELECT * FROM Products WHERE Name = ?', (pname,))
	prod_dets = c.fetchone()
	# print(row)
	c.execute('SELECT * FROM Reviews WHERE PName = ?', (pname.lower(),))
	reviews = c.fetchall()
	# print(reviews)
	context = {'prod':prod_dets, 'reviews':reviews, 'signed_in': logged_in,'uname':user_name}

	return render(request, 'product.html', context)

def sort_home(request):
	if request.COOKIES['user_name']:
		user_name = request.COOKIES['user_name']
	sort_param = request.GET['sort']
	if sort_param == 'rat':
		prod_dict = rating_sort_get()
		prod_dict['uname'] = user_name
		return render(request, 'home.html', prod_dict)
	elif sort_param == 'rev':
		prod_dict = review_sort_get()
		prod_dict['uname'] = user_name
		return render(request, 'home.html', prod_dict)
	elif sort_param == 'old':
		prod_dict = products_from_db()
		prod_dict['products'].reverse() #= reversed(prod_dict['products'])
		prod_dict['uname'] = user_name
		return render(request, 'home.html', prod_dict)
	else:
		prod_dict = products_from_db()
		prod_dict['uname'] = user_name
		return render(request, 'home.html', prod_dict)


def register(request):
	connect = sqlite3.connect("db.sqlite3")
	c = connect.cursor()
	c.execute('SELECT Username FROM Users')
	temp = c.fetchall()
	unames = [x[0] for x in temp]
	if request.method == 'POST':
		uname = request.POST['temp_uname']
		pass1 = request.POST['temp_pass']
		pass2 = request.POST['temp_pass_rep']
		if (uname in unames):
			return render(request, 'register.html', {'alr_reg':True})
		elif pass1 != pass2:
			return render(request, 'register.html', {'pass_match':False})
		else:
			c.execute("INSERT INTO Users VALUES(?,?)", (uname,pass1,))
			connect.commit()
			return render(request, 'shopoholic/login/')
	return render(request, 'register.html')



