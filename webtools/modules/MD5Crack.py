# -*- coding: utf-8 -*-
import cookielib
import socket
import urllib
import urllib2
from bs4 import BeautifulSoup

class Cmd5(object):


    def __init__(self, url,headers=None):
        """
        url格式：http://www.xmd5.org/
        """
        
 
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
            conn = self.opener.open(url)
            conn.info()  # retrieve session cookie
        except Exception, e:
            print e




    def search(self,keyword):
        if not keyword:
            return None
        keyword = keyword.encode('utf-8')
        parameters = {
        "hash" : keyword,
        "xmd5" : "MD5+%BD%E2%C3%DC"
            }
        url = "http://www.cmd5.com/md5/search.asp?"
        url+="hash=%s" %keyword
        url+='&xmd5=MD5+%BD%E2%C3%DC'
#         /md5/search.asp?hash=098950fc58aad83&xmd5=MD5+%BD%E2%C3%DC
        try:
            request=urllib2.Request(url)
            conn=urllib2.urlopen(request)
            page = conn.read()
#             f=open("cmd5.html",'w')
#             f.write(page)
#             f.close()
            code = conn.code
            status = conn.msg
            responseHeaders = conn.info()

        except Exception, e:
            print e
            return None


        
        soup=BeautifulSoup(page)
        soupDiv=soup.find_all(name="table", attrs={"id":'table3'})
        item =soupDiv[0]
        passit=item.find_all(name="span",attrs={'id':'ctl00_ContentPlaceHolder1_LabelAnswer'})
        password=passit.get_text()
        print password
#         retVal = []
#         soup = BeautifulSoup(page)
#         soupDiv = soup.find_all(name="h3")
#         for item in soupDiv:
#             webhref = item.a["href"]
#             webname = item.get_text()
#             req = urllib2.Request(webhref)
#             try:
#                 reurl = urllib2.urlopen(req, timeout=5)
#                 if "baidu" not in reurl.url:
#                     retVal.append((webname, reurl.url))
#             except Exception, e:
#                 print e       
#         return retVal
    
if __name__ == "__main__":
    cmd5 = Cmd5('http://www.cmd5.com/')
    urldict = cmd5.search("098950fc58aad83")
    print urldict

