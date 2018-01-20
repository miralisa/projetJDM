#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import codecs
import requests
import urllib
import time
import os
import HTMLParser

ht = HTMLParser.HTMLParser()
file = codecs.open("motsFrequents.txt", "r", "utf-8")
motsFrequents = [ht.unescape(mot[:-1]) for mot in file]
file.close()

tempsTotal = 0
i = 1
timeout = []
notexists = []
jdmhs = []

for mot in motsFrequents :
	deb = time.time() 
	nLatin = urllib.quote(mot)

	print mot
	r = requests.get("http://localhost:5000/noeud/"+nLatin, timeout=240)

	if r.text == "ERROR":
		print "ERROR"
		break

	if r.text == "TIME-OUT":
		timeout.append(mot)
		print mot+" : TIMEOUT"
	elif r.text == "NOT-EXISTS":
		notexists.append(mot)
		print mot+" : NOT EXISTS"
	elif r.text == "JDM-HS":
		jdmhs.append(mot)
		print mot+" : JDM HS"
	else:
		print "Ok"
	tempsTotal += time.time() - deb

print "Temps total : "+str(tempsTotal)+"s"
print "Temps relatif : "+str(tempsTotal/45)+"s"

