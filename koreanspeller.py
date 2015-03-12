#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import re

class KoreanSpeller:

    def __init__(self, text):
        self.text = text

    def spellcheck(self):
        params = urllib.urlencode({'text1': self.text})

        try:
            f = urllib.urlopen('http://164.125.36.75/PnuSpellerISAPI_201107/lib/PnuSpellerISAPI_201107.dll?Check', params)
            content = f.read()
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)

        self.text = self.text.decode('utf8')

        items = []
        p = re.compile("<table border='1'.*?>(.*?)</table>", re.DOTALL)
        tables = p.findall(content)
        if not tables:
            return items

        position = 0 # match position
        p2 = re.compile('<td.*?>(.*?)</td>', re.DOTALL)
        for table in tables:
            item = {}
            m2 = p2.findall(table)
            s1 = re.compile('<.*?br/>')
            mykey = { 1:'incorrect', 3:'correct', 5:'comment' }
            for index, td in enumerate(m2):
                if index in mykey.keys():
                    td = s1.sub("\n", td)
                    td = td.strip()
                    item[mykey.get(index)] = td

            p3 = re.compile(str(item.get('incorrect')).decode('utf8'))
            m3 = p3.search(self.text, pos=position)
            item['position'] = m3.start()
            position = m3.end()

            items.append(item)

        return items

# 사용법 python koreanspeller.py "안뇽하세요? 방갑습니다."
if __name__ == '__main__':
    import sys

    #s = KoreanSpeller( "안뇽하세요? 방갑습니다." )
    s = KoreanSpeller( sys.argv[1] )
    for item in s.spellcheck():
        print item.get('position')
        print item.get('incorrect') + ' -> ' + item.get('correct')
        print item.get('comment')
        print '---------------------------------------------------'

