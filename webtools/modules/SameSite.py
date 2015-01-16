# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import webbrowser 
import urllib2
import threading
import Queue
from AiZhan import AiZhan

class SameSite(QtGui.QWidget):
    def __init__(self,parent=None):
        super(SameSite,self).__init__(parent)
        self.CBBox=QComboBox()
        self.LEurl=QtGui.QLineEdit()
        self.LWweb=QtGui.QListWidget()
        self.PBSearch=QtGui.QPushButton(u"查询")
        self.CBBox.addItem("aizhan")
        self.CBBox.addItem("360")
        grid=QGridLayout()
        grid.addWidget(self.CBBox,0,0,1,1)
        grid.addWidget(self.LEurl,0,1,1,6)

        grid.addWidget(self.PBSearch,0,7,1,1)
        vbox=QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addWidget(self.LWweb)
        
        self.setLayout(vbox)
        
        self.QABrow = QAction("browser", self)
        self.QACopy = QAction("copy", self)
        self.QASave = QAction("save_all", self)
        self.QABrow.triggered.connect(self.brower)
        self.QACopy.triggered.connect(self.copy)
        self.QASave.triggered.connect(self.save)
        
        self.content = QMenu()
        self.content.addAction(self.QABrow)
        self.content.addAction(self.QACopy)
        self.content.addAction(self.QASave)  
        
        self.connect(self.PBSearch, SIGNAL('clicked()'), self.search)
        
        self.ClassSearch=None
        self.que=Queue.Queue()
        
    def contextMenuEvent(self, event):
        if self.LWweb.count()>0:
            self.content.exec_(QCursor.pos())
    
    def search(self):
        self.LWweb.clear()
        s = self.CBBox.currentText()
        if s == "aizhan":
            self.ClassSearch = AiZhan()
        keyword = unicode(self.LEurl.text())
        result=self.ClassSearch.search(keyword)
                
        for i in xrange(20):
            t = threading.Thread(target=self.addurl)
            t.start()
        if result:
            for url in result:
                self.que.put(url)
        
    def addurl(self):
        while True:
            url=self.que.get()
            item=QListWidgetItem()
            item.setText(url)
            if not self.checkurl(url):
                color=QtGui.QColor()
                color.setRgb(255,0,0)
                item.setTextColor(color)               
            self.LWweb.addItem(item)
            self.que.task_done()
     
    def checkurl(self,url):
        weburl="http://"+url.encode('gbk')
        try:
            request=urllib2.Request(weburl)
            response=urllib2.urlopen(request)
#             print response
            return True
        except:
#             print "wrong"
            return False


    def copy(self):
        clipboard = QApplication.clipboard()
        text = self.LWweb.currentItem().text() 
        clipboard.setText(text)
        
    def save(self):
        filename = QFileDialog.getSaveFileName(self, QString("save file"), './')
        if filename:
            f = open(filename, 'w')
            for i in range(self.LWweb.count()):
                item = self.LWweb.item(i)
                txt = item.text()
                f.write(txt)
                f.write("\n")
            f.close()       
    def brower(self):
        if self.LWweb.currentItem():
            url = self.LWweb.currentItem().text()
            webbrowser.open(url)   

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = SameSite()
    form.show()
    sys.exit(app.exec_())