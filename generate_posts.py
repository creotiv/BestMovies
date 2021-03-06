import requests
import sys
import csv
import re
import json
from datetime import date

tpl = '''---
layout: post
title: {title}
categories: []
tags: []
---
![{title}]({img})
'''

def generate(ids_path):
	with open(ids_path) as fp:
		ids = json.loads(fp.read())
   
	_date = "2018-10-11"
	for id in ids:
		id = 'https://www.imdb.com/title/%s/' % id
		print(id)
		res = requests.get(id, headers={'Accept-Language': 'en-US,en;q=0.9'})
		res = res.content.decode('utf-8')
		img = re.findall(r'class="poster">.*?src="([^"]+)', res, re.M | re.I | re.U | re.S)[0]
		img = "%s_V1.jpg" % img.split('_')[0]
		title = re.findall(r'<h1[^>]+>([^"]+)&nbsp;', res, re.M | re.I | re.U | re.S)[0]
		titleOrig = re.findall(r'<div class="originalTitle">.*?([^<]+)', res, re.M | re.I | re.U | re.S)
		tl = len(re.sub(r'[^a-zA-z0-9]+','',title).strip())
		title = titleOrig[0] if tl < 5 else title
		title = title.replace(':','')
		data = tpl.format(img=img, title=title)
		print(repr(title))
		path = "%s-%s.md" % (_date, re.sub(r'[^a-zA-z0-9]+','-',title.lower().strip()).strip('-'))
		print(path)
		with open('_posts/%s' % path, 'wb') as fp:
			fp.write(data.encode('utf-8'))
   
if __name__ == "__main__":
    generate(sys.argv[1])