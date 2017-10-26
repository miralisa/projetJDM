#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, jsonify, json, request
from neo4j.v1 import GraphDatabase, basic_auth
import codecs
import time

app = Flask(__name__)

driver = GraphDatabase.driver("bolt://192.168.1.72:7687",
	auth=basic_auth("neo4j", "l&!j3ssn&prt3c3"))

session = driver.session()

def allRelations():
    dicoRel = {}
    relations = session.run("MATCH (r:Relation) RETURN r.name, r.info")
    for r in relations:
        #info = r["r.info"].split(" ")
        #if len(info) > 10:    
        dicoRel.update({r["r.name"] : r["r.info"]})
    return dicoRel


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
