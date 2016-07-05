#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


def ddg_search(term):
        url = 'https://duckduckgo.com/html/?q=' + term
        return BeautifulSoup(requests.get(url).text)


def ddg_crawl(bs):
        divs = bs.findAll('div',
                          {'class':
                           lambda x: x
                           and 'result' in x.split()
                          })
        for d in divs:
                if "result--ad" in d["class"]:
                        continue
                children = d.findChildren('a')
                return children[0]['href']
        return ""
