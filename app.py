#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, jsonify, json, request
from neo4j.v1 import GraphDatabase, basic_auth
import codecs
import time
import requests
app = Flask(__name__)

#driver = GraphDatabase.driver("bolt://192.168.1.72:7687",
#	auth = basic_auth("neo4j", "l&!j3ssn&prt3c3"))

#session = driver.session()


def allRelations():
    dicoRel = {}
    relations = session.run("MATCH (r:Relation) RETURN r.name, r.info")
    for r in relations:
        dicoRel.update({r["r.name"][1:-1] : r["r.info"][1:-1]})
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
		if ">" not in record["a.n"] and ":r" not in record["a.n"]:
			resultatas.append(record["a.n"][1:-1])# record["a.eid"]+"|"+record["a.n"]+"|"+record["a.t"]+"|"+record["a.w"]
	return resultatas	

def getDescription(nodeN, ind):
	description = []
	relations = relationsForNode(nodeN)
	size = len(relations)
	if  size != 0 and ind < size:
		description = nodesByRelations(nodeN, relations[ind])
	return description

@app.route('/search_term/')
def searchTerm():
	term = json.loads(request.args.get('term'))
	relations = relationsForNode(term)
	size = len(relations)
	result = ""
	ind = 0
	if size != 0 and ind < size:
		result = nodesByRelations(term, relations[ind])
	#print relations
	return jsonify(relations = relations, result = result)


@app.route('/relation_term/')
def relationTerm():
	term = json.loads(request.args.get('term'))
	relation = json.loads(request.args.get('relation'))
	result = nodesByRelations(term, relation)
	return jsonify(result = result)

""" Render template index.html"""
@app.route('/')
def index():
    relations = allRelations()
    #print relations
    return render_template('index.html', relations = relations)

"""
@app.route('/relations')
def show_relations():
    return render_template('relations.html')
"""

if __name__ == '__main__':
    app.run(debug=True, port=5000)
