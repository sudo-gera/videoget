

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen as u
from urllib.parse import unquote as uqu
from json import loads as l
from sys import argv
import os
import random
from urllib.request import urlopen
from json import loads
from json import dumps
from urllib.parse import quote
from time import sleep
from time import time
from time import asctime
from traceback import format_exc as error
from os import popen
from random import shuffle
from os.path import exists
from os.path import abspath
from os import chdir
#import requests
from random import randint
from urllib.request import urlopen
from json import loads
from json import dumps
from urllib.parse import quote
from time import sleep
from time import time
from time import asctime
from traceback import format_exc as fo
from os import popen
from os import system
from os.path import abspath
from webbrowser import open as webopen
from sys import argv

try:
    url = open('url').read()
except BaseException:
    url = popen('cat ~/url').read()
token = url.split('#')[1].split('&')[0].split('=')[1]


def api(path, data=''):
    if path and path[-1] not in '&?':
        if '?' in path:
            path += '&'
        else:
            path += '?'
    sleep(1 / 6)
    data = data.encode()
    global token
    ret = loads(
        urlopen(
            'https://api.vk.com/method/' +
            path +
            'v=5.101&access_token=' +
            token,
            data=data).read().decode())
    return ret


def com(a):
    q = list(a['title'])
    for e in range(len(q)):
        if not q[e] in '1234567890':
            q[e] = '-'
    q = ''.join(q).split('-')
    q = [int(w) for w in q if w]
    return q + [-a['duration'], 0, 0, 0, 0, 0, 0, 0]


if len(argv) < 2:
    argv = [argv[0], 0]
    print('search mode longer server maxq')
    exit()
skey = argv[1]
if len(argv) >= 3:
    mode = argv[2]
else:
    mode = 'web'
if mode not in 'url web txt'.split():
    print('uncnown mode')
    exit()
if len(argv) >= 4:
    longer = str(eval(argv[3]))
else:
    longer = '0'
if len(argv) >= 5:
    serv = eval(argv[4])
else:
    serv = 0
if len(argv) >= 6:
    maxq=eval(argv[5])
else:
    maxq=float('inf')
if len(argv) >= 7:
    file = argv[6]
else:
    file = {'txt': 'tmp.sh', 'url': 'tmp.html', 'web': 'tmp.html'}[mode]

ban = '|/ ()\t\n\\\"\''


def clear(q):
    return ''.join(['_' if w in ban else w for w in q])


def run(skey, longer):
    q = sum([api('video.search', 'q=' +
                 skey +
                 '&count=200&offset=' +
                 str(w *
                     200) +
                 '&sort=2&adult=1&longer=' +
                 str(eval(longer)))['response']['items'] for w in range(5)], [])
# q=sum([api('video.search','q='+skey+'&count=200&offset='+str(w*200)+'&sort=2&adult=1&filters=mp4&longer='+longer)['response']['items'] for w in range(5)],[])
    q.sort(key=com)
    c = 0
    ext = []
    for w in q:
        c += 1
        t = w['title']
        if 'image' in w:
            img = w['image'][0]['url']
        else:
            img = ''
        t = clear(t)
        if 'files' not in w:
            f = dict()
        else:
            f = w['files']
        d = w['duration']
        global maxq
        while list(f.keys()) and (
#                '.vkuservideo.net' not in f[list(f.keys())[-1]] or
                'mp4_' not in list(f.keys())[-1]
                or eval(list(f.keys())[-1][list(f.keys())[-1].index('mp4_')+4:])>maxq
                ):
            #   print(f[list(f.keys())[-1]])
            del(f[list(f.keys())[-1]])
    # if not arg:
    #  l=list(f.keys())
    #  if not all(['mp4_' in w for w in l]):
    #   print('\x1b[32m',l,'\x1b[0m')
        if list(f.keys()):
            # if 1:
            ext += [[img, c, d, t, f[list(f.keys())[-1]]]]
    return ext


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        path = self.path.split('?', 1)[1:] + ['']
        path = path[0]
        path = path.split('&')
        path = [w.split('=') + [''] for w in path]
        path = [(uqu(w[0].replace('+', ' ')), uqu(w[1].replace('+', ' ')))
                for w in path]
        path = dict(path)
        global longer, skey
        if 'longer' in path:
            longer = path['longer']
            # longer=longer[:3]
        # longer=list(map(int,longer))
    #  longer=longer[0]*3600+longer[1]*60+longer[2]
#   longer=str(longer)
        if 'skey' in path:
            skey = path['skey']
        ext = run(skey, longer)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write('''
  <form>
   <textarea name="skey">{}</textarea>
   <textarea name="longer">{}</textarea>
   <input type="submit" value="search">
  </form>
  '''.format(skey, longer).encode())
        self.wfile.write(('<html><body>').encode())
        for w in ext:
            u, c, d, t, f = w
            self.wfile.write(('<a href=' +
                              f +
                              ' download><img src=' +
                              u +
                              '>' +
                              str(d //
                                  3600) +
                              ':' +
                              str(d %
                                  3600 //
                                  60) +
                              ':' +
                              str(d %
                                  60) +
                              '\t' +
                              t +
                              '.mp4</a><br>\n<pre>' +
                              '-' *
                              12800 +
                              '</pre>\n<br>').encode())
        self.wfile.write('<!DOCTYPE html></body></html>'.encode())


if serv:
    hostPort = 2000
    hostName = '127.0.0.1'
    st = 1
    while st:
        try:
            myServer = HTTPServer((hostName, hostPort), MyServer)
            st = 0
        except BaseException:
            hostPort += 1
    if mode == 'url':
        print('http://127.0.0.1:{}'.format(hostPort))
    if mode == 'web':
        webopen('http://127.0.0.1:{}'.format(hostPort))
    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass

    myServer.server_close()
    print()
    exit()

else:
    ext = run(skey, longer)

if mode == 'txt':
    a = open(file, 'w')
    a.write('# оставьте только те строки, которые должны быть скачаны, имя можно поменять на то, под которым должен сохраниться файл,\n')
    a.write('# остальные уберите полностью или добавьте символ # в начало\n')
    for w in ext:
        u, c, d, t, f = w
        a.write(str(c) + '\t' + str(d // 3600) + ':' + str(d % 3600 // 60) + ':' + str(d % 60) + '\t' + t + '\n')
    a.close()
    system('nano ' + file)
    ch = [w.split() for w in open(file).read().split('\n') if w.split()]
    ch = [[eval(w[0])] + w[1:] for w in ch if w[0].isdigit()]
    names = dict()
    for w in ch:
        if len(w) > 2:
            names[w[0]] = clear(w[2])
        else:
            names[w[0]] = None
    ch = [w[0] for w in ch]
    a = open(file, 'w')
    for w in ext:
        u, c, d, t, f = w
        if c in ch:
            if names[c] is not None:
                t = names[c]
            a.write('wget "' + f + '" -O "' + t + '.mp4"\n')
    a.close()

if mode in ['url', 'web']:
    a = open(file, 'w')
    a.write('<html><body>')
    for w in ext:
        u, c, d, t, f = w
        a.write('<a href=' +
                f +
                ' download><img src=' +
                u +
                '>' +
                str(d //
                    3600) +
                ':' +
                str(d %
                    3600 //
                    60) +
                ':' +
                str(d %
                    60) +
                '\t' +
                t +
                '.mp4</a><br>\n<pre>' +
                '-' *
                12800 +
                '</pre>\n<br>')
    a.write('<!DOCTYPE html></body></html>')
    a.close()
    absp = abspath(file)
    if mode == 'web':
        webopen(absp)
        sleep(8)
    else:
        if absp[0] == '/':
            absp = absp[1:]
        print('file:///' + absp)
