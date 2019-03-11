from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import sqlite3


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
			return render(request, 'home.html', {'uname': user_name})

	return render(request, 'login.html')



