#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#from __future__ import unicode_literals
from neo4j.v1 import GraphDatabase, basic_auth
import codecs
import time
#from elasticsearch import Elasticsearch


driver = GraphDatabase.driver("bolt://192.168.1.72:7687",
	auth=basic_auth("neo4j", "l&!j3ssn&prt3c3"))

session = driver.session()

def allRelations():
	dicoRel = {}
	relations = session.run("MATCH (r:Relation) RETURN r.name, r.info")
	for r in relations:
		dicoRel.update({r["r.name"] : r["r.info"][1:-1]})
	return dicoRel


def relationsForNode(nodeN):
	nodeName = "\"" + nodeN + "\""
	idRelations = []
	foundRelations = []
	result = session.run("MATCH (b:Noeud)-[c:LINKED]->(a:Noeud) WHERE b.n = {name} RETURN distinct c.t ", {"name": nodeName})
	for record in result:
		idRel =  record["c.t"]
		#if idRel not in idRelations:
		idRelations.append(idRel)

	for idsR in idRelations:
		relations = session.run("MATCH (r:Relation) WHERE r.rtid = {id} RETURN r.name", {"id":idsR})
		for r in relations:
			foundRelations.append(r["r.name"][1:-1])
	return foundRelations


def nodesByRelations(nodeN, relationN):
	print nodeN + " " + relationN
	resultatas = []
	relationName = "\"" +relationN +"\""
	relation = session.run("MATCH (r:Relation) WHERE r.name = {name} RETURN r.rtid", {"name":relationName})
	rtid = ""
	for r in relation:
		rtid = r["r.rtid"]

	nodeName = "\"" + nodeN + "\""
	result = session.run("MATCH (b:Noeud)-[c:LINKED]->(a:Noeud) WHERE b.n = {name} AND c.t = '"+rtid+
		"' RETURN a.eid, a.n, a.t, a.w ORDER BY toInt(a.w) DESC", {"name": nodeName})

	for record in result:
		resultatas.append(record["a.n"])# record["a.eid"]+"|"+record["a.n"]+"|"+record["a.t"]+"|"+record["a.w"]
	return resultatas	

def getDescription(nodeN, ind):
	description = []
	relations = relationsForNode(nodeN)
	size = len(relations)
	if  size!= 0 and ind < size:
		description = nodesByRelations(nodeN, relations[ind])
	return description

print getDescription("chat", 0)
#print nodesByRelations("chat", "r_has_part")
"""
result = session.run("MATCH (b:Noeud)-[c:LINKED]->(a:Noeud) WHERE b.n = {name} AND c.t = '102' RETURN a.eid, a.n, a.t, a.w", {"name": "\"poulet\""})


for record in result:
	print record["a.eid"]+"|"+record["a.n"]+"|"+record["a.t"]+"|"+record["a.w"]
"""
"""
def inserer_relation(relation):
	query = "MERGE (:TypeRelation "+str(relation)+")"
	session.run(query)

def inserer_noeud(noeud):
	query = "MERGE (:Noeud "+str(noeud)+")"
	session.run(query)

def inserer_triplet(triplet):
	eid1 = triplet["n1"]
	eid2 = triplet["n2"]
	rtid = triplet["kind"]
	queryMatch = "MATCH (n1:Noeud),(n2:Noeud),(r:TypeRelation) "+\
	"WHERE n1.eid = "+str(eid1)+" AND "+\
	"n2.eid = "+str(eid2)+" AND "+\
	"r.rtid = "+str(rtid)+\
	"RETURN n1.eid, n2.eid, r.rtid"
	result = session.run(queryMatch)
	if len(result)>0:
		queryMerge = "MERGE (n1:Noeud)-(r:Lien "+str(triplet)+\
		")->(n2.Noeud) WHERE n1.eid = "+eid1+ "AND "+\
		"n2.eid = "+eid2
	else:
		raise Exception('Données corompues', str(triplet))


def test():
	liste_noeuds = []
	liste_noeuds.append({str('eid'):1, str('nom'):str('chat')})
	liste_noeuds.append({str('eid'):2, str('nom'):str('chien')})
	liste_noeuds.append({str('eid'):3, str('nom'):str('autruche')})
	liste_relations = []
	liste_relations.append({str('rtid'):1, str('nom'):str('amitie')})
	liste_relations.append({str('rtid'):2, str('nom'):str('inimitie')})
	liste_triplets = []
	liste_triplets.append({str('rid'):1, str('n1'):1, str('n2'):2, str('kind'):2})
	liste_triplets.append({str('rid'):2, str('n1'):2, str('n2'):3, str('kind'):1})
	for noeud in liste_noeuds:
		inserer_noeud(noeud)
	for relation in liste_relations:
		inserer_relation(relation)
	for triplet in liste_triplets:
		inserer_triplet(triplet)
test()


def main():
	file = open("../jeux2mots/JDM-LEXICALNET-FR/09032017"+
		"-LEXICALNET-JEUXDEMOTS-FR-NOHTML.txt", "r")
	#file = codecs.open("sample.txt", "r", "utf-8")

	#es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
	#fileWrite = codecs.open("test.txt", "w", "utf-8")
	#fileWrite = open("test.txt", "w")

	nbRt = 0
	nbN = 0
	nbR = 0

	debRelations = time.time()
	print "Debut parsage des relations...\n"
	debNoeuds = 0
	debTriplets = 0
	avancement = -1

	#es.indices.delete(index='jeux2mots')

	for l in file:
		line1 = l.decode('latin_1')
		line = line1.strip("\n")
		#line = l.strip("\n")

		if line[0:4]=="rtid":
			chunks = line.split("|")
			rtid = chunks[0].split("=")[1]
			name = chunks[1].split("=")[1].strip("\"")
			nom_etendu = chunks[2].split("=")[1].strip("\"")
			info = chunks[3].split("=")[1].strip("\"")
			#es.index(index='jeux2mots', doc_type='relation', id=rtid, body={'nom':name, 'nom_etendu':nom_etendu, 'info':info}, request_timeout=50)
			nbRt += 1
			if int(nbRt*100/135) > avancement:
				avancement = int(nbRt*100/135)
				print "avancement : "+str(avancement)+"%\n"
		elif line[0:3]=="eid":
			if debRelations != 0:
				print "Fin parsage des relations : "+str(int(time.time()-debRelations))+"\n"
				debRelations = 0
				avancement = -1
				debNoeuds = time.time()
				print "Debut parsage des noeuds...\n"
			chunks = line.split("|")
			eid = chunks[0].split("=")[1]
			name = chunks[1].split("=")[1].strip("\"")
			kind = chunks[2].split("=")[1]
			weight=chunks[3].split("=")[1]
			if len(chunks) > 4:
				vf = chunks[4].split("=")[1]
				#es.index(index='jeux2mots', doc_type='noeud', id=eid, body={'nom':name, 'type':kind, 'poids':weight, 'vf':vf}, request_timeout=50)
			#else :
				#es.index(index='jeux2mots', doc_type='noeud', id=eid, body={'nom':name, 'type':kind, 'poids':weight}, request_timeout=50)
			nbN += 1
			if int(nbN*10000/8686889) > avancement*100:
				avancement = float(int(nbN*10000/8686889))/100
				print "avancement : "+str(avancement)+"%\n"
		elif line[0:3]=="rid":
			if debNoeuds != 0:
				print "Fin parsage des noeuds : "+str(int(time.time()-debNoeuds))+"\n"
				debNoeuds = 0
				avancement = -1
				debTriplets = time.time()
				print "Debut parsage des triplets...\n"
			chunks = line.split("|")
			rid = chunks[0].split("=")[1]
			n1 = chunks[1].split("=")[1]
			n2 = chunks[2].split("=")[1]
			kind = chunks[3].split("=")[1]
			weight = chunks[4].split("=")[1]
			#es.index(index='jeux2mots', doc_type='triplet', id=rid, body={'n1':n1, 'n2':n2, 'type':kind, 'poids':weight}, request_timeout=50)
			nbR += 1
			if int(nbN*10000/154626375) > avancement*100:
				avancement = int(nbN*10000/154626375)/100
				print "avancement : "+str(avancement)+"%\n"
			if avancement == 100:
				print "Fin parsage des triplets : "+str(int(time.time()-debTriplets))+"\n"

	print "nbRel : {}, nbNode : {}, nbTriplet : {}".format(nbRt,nbN,nbR)
	file.close()
"""
#fileWrite.close()

session.close()
