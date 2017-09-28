#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
#from neo4j.v1 import GraphDatabase, basic_auth
import codecs
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

file = codecs.open("JDM-LEXICALNET-FR/09032017"+
	"-LEXICALNET-JEUXDEMOTS-FR-NOHTML.txt", "r", "latin_1")

fileWrite = codecs.open("test.txt", "w", "utf-8")

nbRt = 0
nbN = 0
nbR = 0

for line in file:
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
		fileWrite.write(
			"Relation (id:{}, nom:{}, nom_etendu:{}, info:{})".format(
				rtid,name,nom_etendu,info))
		nbRt += 1
	elif line[0:3]=="eid":
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
		fileWrite.write(
			"Noeud (id:{}, nom:{}, type:{}, poids:{})".format(
				eid,name,kind,weight))
		nbN += 1
	elif line[0:3]=="rid":
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
		fileWrite.write(
			"Triplet (id:{}, noeud1:{}, noeud2:{}, type:{}, poids:{})".format(
				rid,n1,n2,kind,weight))
		nbR += 1	

print "nbRel : {}, nbNode : {}, nbTriplet : {}".format(nbR,nbN,nbR)

file.close()
fileWrite.close()

#session.close()