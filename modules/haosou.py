import cookielib
import socket
import urllib
import urllib2
from bs4 import BeautifulSoup

class Haosou(object):
    """
    This class defines methods used to perform 360 dorking 
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
            conn = self.opener.open("http://www.haosou.com")
            conn.info()  # retrieve session cookie
        except urllib2.HTTPError, e:
            e.info()
        except urllib2.URLError:
            errMsg = "unable to connect to Google"

    def search(self, keyword, page=1):
        """
        default page is 1
        """

        gpage = str(page)


        if not keyword:
            return None
        keyword = keyword.encode('utf-8')
#         http://www.haosou.com/s?ie=utf-8&shb=1&src=360sou_newhome&q=test
#         http://www.haosou.com/s?q=test&pn=2&j=0&ls=0&src=srp_paging&fr=360sou_newhome&psid=65807ef41352a73bb16b1148013d83f8
        dataDict = {
            'ie'     :      'utf-8',
            'q'     :      keyword,  # keyword
            'pn'      :     gpage
            }
        url = "http://www.haosou.com/s?"
        Data = urllib.urlencode(dataDict)
        url += (Data)

        try:
            conn = self.opener.open(url)
            page = conn.read()
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

        print len(soupDiv)
        for item in soupDiv:
            try:
                webhref = item.a["href"]
                webname = item.get_text()
            except TypeError:
                print "TypeError"
            if "haosou" not in webhref and  "360.cn" not in webhref:
                retVal.append((webname, webhref))
        return retVal
    
if __name__ == "__main__":
    haosou = Haosou()
    urldict = haosou.search("test", 2)
    print urldict

