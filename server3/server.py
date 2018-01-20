#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from flask import Flask, render_template, jsonify, json, request
import codecs
from flask_mysqldb import MySQL
import requests
import urllib
from bs4 import BeautifulSoup
import json
import time
from random import randint
import HTMLParser
#import base64

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'lf3bf,3jnr'
app.config['MYSQL_DB'] = 'jdm'
mysql = MySQL(app)

file = codecs.open("relations.txt", "r", "utf-8")
relations = [mot[:-1] for mot in file]
file.close()

ht = HTMLParser.HTMLParser()
file = open("motsFrequents.txt", "r")
motsFrequents = [ht.unescape(w)[:-1] for w in file]
file.close()

"""
On implémente un cache LRU 1 bit
"""
TAILLE_CACHE = 100
places_libres = 100
hash_table = {}
entrees_cache = [None for i in range(0,TAILLE_CACHE)]
mru = None


def recupererMot(mot):
	global places_libres
	debut = time.time()
	tab = hash_table.get(mot)

	if tab != None :
		data = recupererBDD(tab[1])
		mru = tab[0]	
	elif places_libres != 0:
		try:
			data = ajouterBDD(mot)
			if data != "JDM-HS" and data != "NOT-EXISTS" and data!="TIME-OUT":
				indice = 100 - places_libres
				places_libres -= 1
				ajouterMotCacheIndice(mot, data['noeud']['eid'], indice)
		except Exception:
			raise
	else:
		try :
			data = ajouterBDD(mot)
			if data != "JDM-HS" and data != "NOT-EXISTS" and data!="TIME-OUT":
				indice = enleverEntreeCache()
				ajouterMotCacheIndice(mot, data['noeud']['eid'], indice)
		except Exception :
			raise
	fin = time.time()
	print "@-- Temps total : "+str(fin-debut)+"s --@"
	return data

def ajouterMotCacheIndice(mot, eid, indice):
	entrees_cache[indice] = mot
	hash_table[mot] = (indice,eid)
	mru = indice


def enleverEntreeCache():
	indice = randint(0,TAILLE_CACHE-1)
	while indice == mru :
		indice = randint(0,TAILLE_CACHE-1)
	mot = entrees_cache[indice]
	eid = hash_table[mot][1]
	entrees_cache[indice] = None
	hash_table[mot] = None
	enleverBDD(eid)
	return indice


def ajouterBDD(mot):
	debut = time.time()
	nLatin = urllib.quote(mot.encode("latin-1"))

	m_text = None

	if mot not in motsFrequents:
		try :
			r = requests.get("http://www.jeuxdemots.org/rezo-xml.php?"+
				"gotermsubmit=Chercher&gotermrel="+nLatin+
				"&output=onlyxml", timeout=180)
		except:
			print "@-- TIME OUT --@"
			return "TIME-OUT"

		fin = time.time()
		print "@-- Requete vers JDM du mot "+mot+" : "+str(fin-debut)+"s --@"

		if len(r.text) == 0:
			print "@-- Jeuxdemots HS --@"
			return "JDM-HS"
		m_text = r.text
	else :
		#mot2 = base64.urlsafe_b64encode(mot)
		mot2 = mot
		if mot == '***':
			mot2 = 'etoileetoileetoile'
		file = open("motsFrequents/"+mot2, "r")
		m_text = file.read()
		fin = time.time()
		print "@-- Lecture du fichier motsFrequents/"+mot2+" : "+str(fin-debut)+"s --@"
		file.close()


	debut = time.time()
	entrant = {}
	sortant = {}

	soup = BeautifulSoup(m_text, "lxml")

	if soup.find("mot") == None:
		print "@-- Le mot "+mot+" n'existe pas --@"
		return "NOT-EXISTS"

	defi = soup.find("def").decode_contents()
	
	if len(defi)>20000:
		print mot+" a une definition de taille "+str(len(defi))+", incroyable !"
		defi = defi[:20000]
	
	mt = soup.find("mot")
	eid =  int(mt.get('id'))
	#print "eid : "+str(eid)
	weight = int(mt.get('poids'))
	nf = soup.find("mot-formate").decode_contents()

	en_temp = soup.find("entrant")
	if en_temp != None:
		en = en_temp.findChildren()
	else :
		en = []
	for rel in en:
		poids = int(rel.get('poids'))
		relation = rel.get('type') 
		name = rel.decode_contents()


		if relation not in entrant.keys():
			entrant[relation] = []
		entrant[relation].append({
				'n2': eid,
				'name': name,
				'w': poids
			})
	so_temp = soup.find("sortant")
	if so_temp != None :
		so = so_temp.findChildren()
	else:
		so = []
	for rel in so:
		poids = int(rel.get('poids'))
		relation = rel.get('type') 
		name = rel.decode_contents()
		"""
		if len(name) > len('animal') and name[-6:]=="animal":
			print name
			print type(name)
		"""

		if relation not in sortant.keys():
			sortant[relation] = []
		sortant[relation].append({
				'n1': eid,
				'name': name,
				'w': poids
			})

	data = {
		'noeud': {
			'eid': eid,
			'name': mot,
			'weight': weight,
			'definition': defi,
			'nf': nf
		},
		'entrant': entrant,
		'sortant': sortant
	};
	
	fin = time.time()
	print "@-- Parsage de la réponse de JDM : "+str(fin-debut)+"s --@"

	debut = time.time()
	try :
		conn = mysql.connection 
		cur = conn.cursor()
		cur.execute("set names utf8;")
		querynoeud = """INSERT INTO noeuds (eid, name, weight, definition, nf) VALUES (%(eid)s,%(name)s,%(weight)s,%(definition)s,%(nf)s);"""
		#print data['noeud']
		cur.execute(querynoeud, data['noeud'])

		for rel, vals in data['entrant'].items():
			nom_table = rel.replace("-","_").replace(">","_")+"_entrant"
			cur.executemany("INSERT INTO "+nom_table+" (n2,name,w) VALUES (%(n2)s,%(name)s,%(w)s)",\
				vals)

		for rel, vals in data['sortant'].items():
			nom_table = rel.replace("-","_").replace(">","_")+"_sortant"
			cur.executemany("INSERT INTO "+nom_table+" (n1,name,w) VALUES (%(n1)s,%(name)s,%(w)s)",\
				vals)
		conn.commit()
	except:
		raise
	fin = time.time()
	print "@-- Insertion du mot dans BDD : "+str(fin-debut)+"s --@"
	return data



def enleverBDD(eid):
	debut = time.time()
	conn = mysql.connection 
	cur = conn.cursor()
	for rel in relations:
		nom_table_entrant = rel.replace("-","_").replace(">","_")+"_entrant"
		nom_table_sortant = rel.replace("-","_").replace(">","_")+"_sortant"
		cur.execute("delete from "+nom_table_entrant+" where n2 = "+str(eid))
		cur.execute("delete from "+nom_table_sortant+" where n1 = "+str(eid))
	cur.execute("delete from noeuds where eid = "+str(eid))
	conn.commit()
	fin = time.time()
	print "@-- Suppression de l'entrée "+str(eid)+" de la BDD : "+str(fin-debut)+"s --@"

def recupererBDD(eid):
	debut = time.time()
	conn = mysql.connection 
	cur = conn.cursor()

	cur.execute("""SELECT * FROM noeuds where eid = %s""",(eid,))
	noeud_temp = cur.fetchone()
	noeud = {
		'eid': noeud_temp[0],
		'name': noeud_temp[1],
		'weight': noeud_temp[2],
		'definition': noeud_temp[3],
		'nf': noeud_temp[4]
	}
	entrant = {}
	sortant = {}
	for rel in relations :
		nom_table_entrant = rel.replace('-', '_').replace('>', '_')+"_entrant"
		nom_table_sortant = rel.replace('-', '_').replace('>', '_')+"_sortant"

		cur.execute("SELECT * FROM "+nom_table_entrant+" WHERE n2 = "+str(eid))
		rels_temp = cur.fetchall()
		rels = [{'n2':row[0], 'name':row[1], 'w':row[2]} for row in rels_temp]
		if len(rels)>0:
			entrant[rel]=rels

		cur.execute("SELECT * FROM "+nom_table_sortant+" WHERE n1 = "+str(eid))
		rels_temp = cur.fetchall()
		rels = [{'n2':row[0], 'name':row[1], 'w':row[2]} for row in rels_temp]
		if len(rels)>0:
			sortant[rel]=rels
	conn.commit()
	fin = time.time()
	print "@-- Recuperation du mot "+noeud['name']+" à partir de BDD : "+str(fin-debut)+"s --@"
	return {
		'noeud': noeud,
		'entrant': entrant,
		'sortant': sortant
	}


@app.route('/')
def index():
	#debut = time.time()
	#data = ajouterBDD("chat")
	#enleverEntree(150)
	"""
	data = recupererBDD(150)
	fin = time.time()
	print "Temp d'execution : "+str(fin-debut)+"s"
	return json.dumps(data, indent=4, ensure_ascii=False)
	"""
	#enleverEntree()
	return 'coucou'

@app.route('/timeout')
def to():
	time.sleep(10)
	return "TIME-OUT"

"""
@app.route('/listenoeudsfrequents')
def liste_noeuds_plus_frequents():
    return "chat, chien ..."

#TODO
@app.route('/listerelations'):
def liste_relations():
	return "r_associated, r_can_eat ..."
"""
@app.route('/initialiser')
def initialiser():
	global places_libres
	debut = time.time()
	conn = mysql.connection 
	cur = conn.cursor()

	cur.execute("SELECT eid, name from noeuds")
	rows = cur.fetchall()
	for row in  rows:
		eid = row[0]
		name = row[1]
		indice = TAILLE_CACHE - places_libres
		places_libres -= 1
		ajouterMotCacheIndice(name, eid, indice)
	return 'Initialisation complete'	


@app.route('/noeud/<string:noeud>')
def recuperer(noeud):
	try:
		data = recupererMot(noeud)
	except Exception as e:
		print e
		return "ERROR"
	if data != "JDM-HS" and data != "NOT-EXISTS" and data!="TIME-OUT":
		return json.dumps(data, indent=4, ensure_ascii=False)
	else:
		return data
"""
#TODO
@app.route('/noeud/relation', methods=['GET'])
def relations()
	noeud = request.args.get('noeud')
	relation = request.args.get('relation')
	return "[]"
"""
if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")