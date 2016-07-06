#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import sys
import re
import classinfo

def get_bs(link):
        return BeautifulSoup(requests.get(link).text)


def get_department_soup(dept="CS"):
        url = "http://resources.utulsa.edu/schedule/2016FA"
        url += dept + ".html"
        return get_bs(url)


def get_class_info(c="PHYS-2063-02", section=''):
        data = c.split('-')
        course = data[0] + " " + data[1]
        if len(data) > 2:
                section = data[2]
        bs = get_department_soup(data[0])
        table = bs.findChild('table')
        rows = table.findChildren('tr')
        for row in rows:
                cells = row.findChildren('td')
                if cells and cells[1].string == course:  # and cells[2].string == data[2]:
                        if section == '' or cells[2].string == section:
                                base_url = "http://resources.utulsa.edu/schedule/"
                                end_url = cells[4].findChild('a')['href']
                                return get_bs(base_url + end_url)




def get_book_info(bs):
        books = []
        tables = bs.findChildren('table')[2:]
        for table in tables:
                book = dict()
                rows = table.findChildren('tr')
                for row in rows:
                        col = row.findChildren('td')
                        key = col[0].string[:-1].replace('\r\n', ' ')
                        book[key] = col[1].string
                books.append(book)
        return books


def do_stuff(data=["PHYS-2063-02",
                   "CS-3003-01",
                   "MATH-4003-01",
                   "CS-4863-01",
                   "CS-2033-01",
                   "PHYS-2061-04"]):
        schedule = dict()
        times = []
        for c in data:
                try:
                        bs = get_class_info(c)
                        schedule[c] = get_book_info(bs)
                        times.extend(classinfo.get_info(bs))
                except:
                        pass
        return schedule, times

if __name__ == "__main__":
        l = []
        pat = re.compile("^[A-Z]{2,4}-\d{4}")
        for line in sys.stdin:
                if pat.match(line):
                        l.append(line.strip())
                else:
                        print("%s: Not valid format" % line.strip())
        data, times = do_stuff(l)
        print(json.dumps(data, indent=4))
        print(json.dumps(times, indent=4))
