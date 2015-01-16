# -*- coding: utf-8 -*-
import cookielib
import socket
import urllib
import urllib2
from bs4 import BeautifulSoup

class Baidu(object):
    """
    This class defines methods used to perform Google dorking (command
    line option '-g <google dork>'
    """

    def __init__(self, headers=None):

        self._cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cj))
        if not headers:
            handers = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'),
                             ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
#                              ('Accept-Encoding', 'gzip,deflate,sdch'),
                              ('Accept-Language', 'zh-CN,zh;q=0.8')
                    ]
        self.opener.addheaders = handers
        urllib2.install_opener(self.opener)


        try:
            conn = self.opener.open("http://www.baidu.com")
            conn.info()  # retrieve session cookie
        except urllib2.HTTPError, e:
            e.info()
        except urllib2.URLError:
            errMsg = "unable to connect to Google"

    def search(self, keyword, page=1):
        """
        default page is 1
        """
        page = int(page) - 1
        gpage = str(page * 10)


        if not keyword:
            return None
        keyword = keyword.encode('utf-8')
#         keyword = urllib.quote(keyword)
        dataDict = {
            'ie'     :      'utf-8',
            'mod'    :      '1',
            'isbd'   :      '1',
            'f'      :      '8',
            'rsv_bp' :      '1',
            'rsv_idx':      '1',
            'wd'     :      keyword,  # keyword
            'rsv_enter':    '0',
            '_ss'     :     '1',
            'pn'      :     gpage
            }
        url = "http://www.baidu.com/s?"
        Data = urllib.urlencode(dataDict)
        url += (Data)

        try:
            conn = self.opener.open(url)
            page = conn.read()
#             f=open("baidu.html",'w')
#             f.write(page)
#             f.close()
            code = conn.code
            status = conn.msg
            responseHeaders = conn.info()

        except urllib2.HTTPError, e:
            try:
                page = e.read()
            except socket.timeout:
                return None
        except (urllib2.URLError, socket.error, socket.timeout):
            print "error"
            return None

        
        
        retVal = []
        soup = BeautifulSoup(page)
        soupDiv = soup.find_all(name="h3")
        for item in soupDiv:
            webhref = item.a["href"]
            webname = item.get_text()
            req = urllib2.Request(webhref)
            try:
                reurl = urllib2.urlopen(req, timeout=5)
                if "baidu" not in reurl.url:
                    retVal.append((webname, reurl.url))
            except Exception, e:
                print e       
        return retVal
    
if __name__ == "__main__":
    baidu = Baidu()
    urldict = baidu.search("test")
    print urldict

