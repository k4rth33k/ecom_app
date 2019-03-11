from django.shortcuts import render
import sqlite3
import sys
sys.path.insert(0, '../')
from global_util import products_from_db

def home(request):
	# connect = sqlite3.connect("db.sqlite3")
	# c = connect.cursor()
	# c.execute('SELECT * FROM Products')
	# products = c.fetchall()
	# prod_dict = {'products':products}
	prod_dict = products_from_db()

	if request.method == 'POST':
		sort_param = request.POST['param']

	return render(request, 'home.html', prod_dict)