from django.shortcuts import render
import sqlite3

def home(request):
	connect = sqlite3.connect("db.sqlite3")
	c = connect.cursor()
	c.execute('SELECT * FROM Products')
	products = c.fetchall()
	prod_dict = {'products':[, ]}
	for i,prod in enumerate(products):
		temp = {}
	if request.method == 'POST':
		sort_param = request.POST['param']

	return render(request, 'home.html', prod_dict)