#!/usr/bin/env python2.7

from __future__ import print_function
import re, sys, markdown, requests, bs4 as BeautifulSoup

try:               # Python 2
    reload
except NameError:  # Python 3
    from importlib import reload

reload(sys)
sys.setdefaultencoding('utf8')

def check_url(url):
    try:
        return bool(requests.head(url, allow_redirects=True))
    except Exception as e:
        print('Error checking URL %s: %s' % (url, e))
        return False

def retrieve_urls(filename):
    with open(filename) as fd:
        mdtext = fd.read()
        html_text = markdown.markdown(mdtext)
        soup = BeautifulSoup.BeautifulSoup(html_text, "html.parser")
        return [a['href'] for a in soup.findAll('a')]

def check_urls(filename):
    print('checking URLs for %s' % filename)
    ok = True
    for url in retrieve_urls(filename):
        r = "(?:http[s]?://[^)]+)"
        u = re.findall(r, url)
        if not u: continue
        msg = 'Checking %s => ' % (u[0],)
        if check_url(u[0]):
            print(msg, 'OK')
        else:
            print(msg, 'FAILED')
            ok = False
    return ok

def main():
    ok = True
    for filename in sys.argv[1:]:
        try:
            ok &= check_urls(filename)
        except IOError as e:
            print(e)
            ok = False
    exit(0 if ok else 1)

if __name__ == '__main__':
    main()
