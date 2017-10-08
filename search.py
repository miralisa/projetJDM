#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

res = es.search(index='jeux2mots', body={"query": {"query_string" : {"query": "chat", "fuzziness" : 2, "default_field": "nom"}}})
print('%d documents found' % res['hits']['total'])
liste_id = []
for doc in res['hits']['hits']:
	liste_id.append(int(doc['_id']))
	
print liste_id
#print liste_highlights


res2 = es.search(index='jeux2mots', body={"query": {"query_string": {"query": liste_id[0], "fields" :["n1", "n2"]}}})
print('%d documents found' % res2['hits']['total'])
liste_nds = []
for doc in res2['hits']['hits']:
	liste_nds.append(doc['_source']['n2'])
	
print liste_nds

noeud_liste = []
for id in liste_nds:
	res3 = es.get(index="jeux2mots", doc_type='noeud', id=id)
	noeud_liste.append(res3['_source']['vf'])
print(noeud_liste)
