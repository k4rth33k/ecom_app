import sqlite3
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import operator
import pprint


logged_in = False

def products_from_db():
	connect = sqlite3.connect("db.sqlite3")
	c = connect.cursor()
	c.execute('SELECT * FROM Products')
	products = c.fetchall()
	prod_dict = {'products':products}
	return prod_dict

def rating_sort_get():
	sorted_prods = []
	connect = sqlite3.connect("db.sqlite3")
	c = connect.cursor()
	c.execute('SELECT * FROM RatingSort')
	sorted_names = c.fetchall()
	for x in sorted_names:
		c.execute('SELECT * FROM Products WHERE Name = ?',(x[0],))
		temp = c.fetchall()
		sorted_prods.append(temp[0])

	prod_dict = {'products':sorted_prods}
	return prod_dict


def rating_sort_do():
	connect = sqlite3.connect("db.sqlite3")
	c = connect.cursor()
	c.execute("DELETE FROM RatingSort")
	prod_names = []
	c.execute('SELECT Name FROM Products')
	temp_names = c.fetchall()
	for x in temp_names:
		prod_names.append(x[0])
	sorted_prods = {}
	for product in prod_names:
		c.execute('SELECT avg(Rating) FROM Reviews WHERE PName = ?',(product.lower(),))
		temp = c.fetchone()
		sorted_prods[product] = temp[0]
	sorted_prods = sorted(sorted_prods.items(), key=operator.itemgetter(1), reverse=True)
	for key,value in sorted_prods:
		c.execute("INSERT INTO RatingSort VALUES(?)", (key,))
		print(key,value)
	connect.commit()


def review_sort_do():
	prod_scores = {}
	connect = sqlite3.connect("db.sqlite3")
	c = connect.cursor()
	c.execute("DELETE FROM ReviewSort")
	prod_names = []
	c.execute('SELECT Name FROM Products')
	temp_names = c.fetchall()
	for x in temp_names:
		prod_names.append(x[0])
	print(prod_names)
	for product in prod_names:
		c.execute('SELECT Review FROM Reviews WHERE PName = ?',(product.lower(),))
		revs = c.fetchall()
		for rev in revs:
			opinion = TextBlob(rev[0], analyzer=NaiveBayesAnalyzer())
			if opinion.sentiment.classification == 'pos':
				if product not in prod_scores.keys():
					prod_scores[product] = 1
				else:
					prod_scores[product] += 1
			else:
				if product not in prod_scores.keys():
					prod_scores[product] = -1
				else:
					prod_scores[product] -= 1

	prod_scores = sorted(prod_scores.items(), key=operator.itemgetter(1),reverse=True)
	# print(prod_scores)
	for key,value in prod_scores:
		c.execute("INSERT INTO ReviewSort VALUES(?,?)", (key,value,))
		print(key,value)
	connect.commit()

def review_sort_do_2(pname, review):
	connect = sqlite3.connect("db.sqlite3")
	c = connect.cursor()
	prod_names = []
	c.execute('SELECT PName FROM ReviewSort')
	temp_names = c.fetchall()
	for x in temp_names:
		prod_names.append(x[0])
	if pname not in prod_names:
		c.execute("INSERT INTO ReviewSort VALUES(?,?)", (pname,0,))
	else:
		c.execute("SELECT Score FROM ReviewSort WHERE PName = ?", (pname,))
		score = c.fetchone()[0]
		opinion = TextBlob(review, analyzer=NaiveBayesAnalyzer())
		if opinion.sentiment.classification == 'pos':
			score += 1
		else:
			score -= 1
		c.execute("UPDATE ReviewSort SET Score = ? WHERE PName = ?",(score,pname,))
		connect.commit()

def review_sort_get():
	sorted_prods = []
	connect = sqlite3.connect("db.sqlite3")
	c = connect.cursor()
	c.execute('SELECT PName FROM ReviewSort ORDER BY Score DESC')
	sorted_names = c.fetchall()
	for x in sorted_names:
		c.execute('SELECT * FROM Products WHERE Name = ?',(x[0],))
		temp = c.fetchall()
		sorted_prods.append(temp[0])

	prod_dict = {'products':sorted_prods}
	return prod_dict

