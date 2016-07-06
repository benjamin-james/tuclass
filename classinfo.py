import time
import re

regex = re.compile(r'^(\w+)\s+(\S+)\s+(\w+)\s+(\d{2}:\d{2}[AP]M)-(\d{2}:\d{2}[AP]M)$')
re_tag = re.compile(r'</?br>')

def get_info(bs):
        table = bs.findChild('table')
        rows = table.findChildren('tr')
        for row in rows:
                col = row.findChildren('td')
                key = col[0].string[:-1].replace('\r\n', ' ')
                if key == 'Meeting Times':
                        info = list(map(str, col[1].contents))
                elif key == 'Course Section Number':
                        name = col[1].string
        data = []
        for s in info:
                d = dict()
                s = re.sub(re_tag, '', s)
                m = regex.match(s)
                if not m:
                        continue
                d['name'] = name
                d['building'] = m.group(1)
                d['room'] = m.group(2)
                d['times'] = []
                days = day_parse(m.group(3))
                for day in days:
                        begin = time.strptime(day + ' ' + m.group(4), '%A %I:%M%p')
                        end = time.strptime(day + ' ' + m.group(5), '%A %I:%M%p')
                        d['times'].append((begin, end))
                data.append(d)
        return data

def day_parse(s):
        l = []
        for i in range(len(s)):
                if s[i] == 'M':
                        l.append('Monday')
                elif s[i] == 'W':
                        l.append('Wednesday')
                elif s[i] == 'F':
                        l.append('Friday')
                elif s[i] == 'T' and i + 1 < len(s) and s[i+1].upper() == 'H':
                        l.append('Thursday')
                elif s[i] == 'T':
                        l.append('Tuesday')
        return l
