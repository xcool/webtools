# -*- coding: utf-8 -*-
import cookielib
import socket
import urllib
import urllib2
import re
import json

class AiZhan(object):
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


#         try:
#             conn = self.opener.open("http://dns.aizhan.com")
#             conn.info()  # retrieve session cookie
#         except urllib2.HTTPError, e:
#             e.info()
#         except urllib2.URLError:
#             errMsg = "unable to connect"

    def search(self, keyword):
        if not keyword:
            return None
        keyword = keyword.encode('utf-8')

        dataDict = {
                    'q':keyword,
            }
        url = "http://dns.aizhan.com/?"
        Data = urllib.urlencode(dataDict)
        url += Data

        try:
            request=urllib2.Request(url)
            conn=urllib2.urlopen(request)
            page = conn.read()

            

        except urllib2.HTTPError, e:
            try:
                page = e.read()
            except socket.timeout:
                return None
        except (urllib2.URLError, socket.error, socket.timeout):
            print "error"
            return None


        ip = re.findall(r'IP地址是  <font color="#008000">(.*)</font> 所在地区为',page)
        if ip:
            ip=ip[0]
        else:
            return None
        dataDict = {
                    'r':'index/domains',
                    'ip':ip,
                    'page':'1'
            }
        url = "http://dns.aizhan.com/index.php?"
        Data = urllib.urlencode(dataDict)
        url += Data
        try:
            request=urllib2.Request(url)
            conn=urllib2.urlopen(request)
            page = conn.read()
            dic=json.loads(page)
            maxpage,retVal=(dic["maxpage"],dic["domains"])
            i=2
            while i<=maxpage:
                dataDict = {
                        'r':'index/domains',
                        'ip':ip,
                        'page':str(i)
                }
                url = "http://dns.aizhan.com/index.php?"
                Data = urllib.urlencode(dataDict)
                url += Data
                try:
                    request=urllib2.Request(url)
                    conn=urllib2.urlopen(request)
                    page = conn.read()
                    dic=json.loads(page)
                    retVal.extend(dic["domains"])
                    i+=1
                except:
                    print "error"

            return retVal
        except:
            print "error"
        
        


            
    
    

        

    
if __name__ == "__main__":
    baidu = AiZhan()
    urldict = baidu.search("www.baidu.com")
    print urldict

