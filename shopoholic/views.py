from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import sqlite3
import sys
sys.path.insert(0, '../')
from global_util import products_from_db,logged_in


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
			logged_in = True
			prod_dict = products_from_db()
			prod_dict['uname'] = user_name
			prod_dict['sort'] = True
			return render(request, 'home.html', prod_dict)

	return render(request, 'login.html')

def product(request):
	pname = request.GET['pname']
	connect = sqlite3.connect("db.sqlite3")
	c = connect.cursor()
	c.execute('SELECT * FROM Products WHERE Name = ?', (pname,))
	prod_dets = c.fetchone()
	# print(row)
	c.execute('SELECT * FROM Reviews WHERE PName = ?', (pname.lower(),))
	reviews = c.fetchall()
	# print(reviews)
	context = {'prod':prod_dets, 'reviews':reviews, 'signed_in': logged_in}

	return render(request, 'product.html', context)




