import sqlite3


logged_in = False

def products_from_db():
	connect = sqlite3.connect("db.sqlite3")
	c = connect.cursor()
	c.execute('SELECT * FROM Products')
	products = c.fetchall()
	prod_dict = {'products':products}
	return prod_dict
