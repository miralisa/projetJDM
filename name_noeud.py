#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import codecs
from flask_mysqldb import MySQL
from flask import Flask

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'lf3bf,3jnr'
app.config['MYSQL_DB'] = 'jdm'
mysql = MySQL(app)


@app.route('/')
def index():
	file = codecs.open("noeuds.txt", "r","utf-8")
	noeuds = []
	for w in file:
		mot = w[:-1]
		noeuds.append(mot)
	conn = mysql.connection
	cur = conn.cursor()
	cur.executemany("""INSERT INTO name_noeud VALUES (%s)""",noeuds)
	conn.commit()
	file.close()
	return "DONE\n"

if __name__ == '__main__':
	app.run(debug=True, port=5000, host="0.0.0.0")

"""
def getline(_file):
	ln = u''
	while True:
		_ln = _file.readline().decode("latin-1")
		ln += _ln
		if not _ln:
			break
		if _ln[-1] == '\n':
			break
	return ln

noeuds = codecs.open("noeuds.txt", "w","utf-8")
jdm = open("09032017-LEXICALNET-JEUXDEMOTS-FR-NOHTML.txt","r")

buff = []
cp = 0
i = 0
termine = False
commence = False
while not commence or not termine:
	line = getline(jdm)
	if line[0:3] == "eid":
		if not commence:
			commence = True
		tab = line.split("|")
		mot = "=".join(tab[1].split("=")[1:])[1:-1]
		buff.append(mot)
		cp += 1
		if cp > 100000:
			i += 1
			for m in buff:
				noeuds.write(m+"\n")
			cp = 0
			buff = []
			print str(i*100000)+"\n"
		#cur.execute("INSERT INTO name_noeud (name) VALUES (\""+mot+"\")")
		#conn.commit()
	elif commence:
		if cp > 0:
			for m in buff:
				noeuds.write(m+"\n")
			print str(i*100000+cp)+"\n"
		termine = True
jdm.close()
noeuds.close() 
"""