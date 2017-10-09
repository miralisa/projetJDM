#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import codecs
import time
import requests
import os


r = requests.get("http://192.168.1.72:5000/definition/vraiment")

print r.text