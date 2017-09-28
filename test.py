#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
#from neo4j.v1 import GraphDatabase, basic_auth
import codecs
import time
from elasticsearch import Elasticsearch

"""
driver = GraphDatabase.driver("bolt://localhost:7687", 
	auth=basic_auth("neo4j", "lifeisadream"))

session = driver.session()
"""
"""
result = session.run("MATCH (a)-[:LIKE]->(b) DELETE a.name, b.name")

for record in result:
	print("%s aime %s" % (record["a.name"],record["b.name"]))
"""

#file = open("JDM-LEXICALNET-FR/09032017"+
#	"-LEXICALNET-JEUXDEMOTS-FR-NOHTML.txt", "r")
file = codecs.open("sample.txt", "r", "utf-8")

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
#fileWrite = codecs.open("test.txt", "w", "utf-8")
#fileWrite = open("test.txt", "w")

nbL = 0
nbRt = 0
nbN = 0
nbR = 0
avancement = 0
deb = time.time()
print "avancement : "+str(avancement)+"%\n"

#es.indices.delete(index='jeux2mots')

relations = True
noeuds = True

for l in file:
	nbL += 1
	#line1 = l.decode('latin_1')
	#line = line1.strip("\n")
	line = l.strip("\n")

	if int(nbL*100/163313713) > avancement:
		avancement = int(nbL*100/163313713)
		print "Interval : "+str(int(time.time()-deb))+"second"
		deb = time.time()
		print "avancement : "+str(avancement)+"%\n"

	if line[0:4]=="rtid":
		chunks = line.split("|")
		if len(chunks) < 4:
			print chunks
			print "relations\n"
			print len(chunks)
			break
		rtid = chunks[0].split("=")[1]
		name = chunks[1].split("=")[1].strip("\"")
		nom_etendu = chunks[2].split("=")[1].strip("\"")
		info = chunks[3].split("=")[1].strip("\"")
		es.index(index='jeux2mots', doc_type='relation', id=rtid, body={'nom':name, 'nom_etendu':nom_etendu, 'info':info}, request_timeout=50)
		"""
		fileWrite.write(
			"Relation (id:{}, nom:{}, nom_etendu:{}, info:{})".format(
				rtid,name,nom_etendu,info))
				"""
		nbRt += 1
	elif line[0:3]=="eid":
		if relations == True :
			relations = False
			print "Fin création des relations : "+str(int(time.time()-deb))+" secondes.\n"
		chunks = line.split("|")
		if len(chunks) < 4:
			print chunks
			print "noeuds\n"
			print len(chunks)
			break
		eid = chunks[0].split("=")[1]
		name = chunks[1].split("=")[1].strip("\"")
		kind = chunks[2].split("=")[1]
		weight=chunks[3].split("=")[1]
		if len(chunks) > 4:
			vf = chunks[4].split("=")[1]
			es.index(index='jeux2mots', doc_type='noeud', id=eid, body={'nom':name, 'type':kind, 'poids':weight, 'vf':vf}, request_timeout=50)
		else :
			es.index(index='jeux2mots', doc_type='noeud', id=eid, body={'nom':name, 'type':kind, 'poids':weight}, request_timeout=50)
		"""
		fileWrite.write(
			"Noeud (id:{}, nom:{}, type:{}, poids:{})".format(
				eid,name,kind,weight))
		"""
		nbN += 1
	elif line[0:3]=="rid":
		if noeuds == True :
			noeuds = False
			print "Fin création des noeuds : "+str(int(time.time()-deb))+" secondes.\n"
		chunks = line.split("|")
		if len(chunks) < 5:
			print chunks
			print "triplets\n"
			print len(chunks)
			break
		rid = chunks[0].split("=")[1]
		n1 = chunks[1].split("=")[1]
		n2 = chunks[2].split("=")[1]
		kind = chunks[3].split("=")[1]
		weight = chunks[4].split("=")[1]
		es.index(index='jeux2mots', doc_type='triplet', id=rid, body={'n1':n1, 'n2':n2, 'type':kind, 'poids':weight}, request_timeout=50)
		"""
		fileWrite.write(
			"Triplet (id:{}, noeud1:{}, noeud2:{}, type:{}, poids:{})".format(
				rid,n1,n2,kind,weight))
		"""
		nbR += 1	
	
print "nbRel : {}, nbNode : {}, nbTriplet : {}".format(nbRt,nbN,nbR)

file.close()
#fileWrite.close()

#session.close()