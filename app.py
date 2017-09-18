#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, jsonify, json, request
from flaskext.mysql import MySQL
import random, json
from elasticsearch import Elasticsearch

app = Flask(__name__)
mysql = MySQL()

file_ids = open("database_identifiers.json","r")
ids = json.load(file_ids)
file_ids.close()

app.config['SECRET_KEY'] = 'secret!'
app.config['MYSQL_DATABASE_USER'] = str(ids['login'])
app.config['MYSQL_DATABASE_PASSWORD'] = str(ids['password'])
app.config['MYSQL_DATABASE_DB'] = str(ids['database_name'])
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_CHARSET'] = 'utf-8'
mysql.init_app(app)

conn = mysql.connect()

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


""" Render template index.html"""
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
