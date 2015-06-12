# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from baidu import Baidu
from haosou import Haosou
import webbrowser 


class UrlGet(QtGui.QWidget):
    def __init__(self,parent=None):
        super(UrlGet,self).__init__(parent)
        self.CBBox=QtGui.QComboBox()

        self.LEkeyword = QtGui.QLineEdit()
        self.PBStart = QtGui.QPushButton()
        self.PBStart.setText(u"开始ʼ")
        self.PBnextpage = QtGui.QPushButton()
        self.PBnextpage.setText(u"下一页")
        self.LWweb = QtGui.QListWidget()
        self.CBBox = QtGui.QComboBox()
        
        grid=QGridLayout()
        grid.addWidget(self.CBBox,0,0,1,1)
        grid.addWidget(self.LEkeyword,0,1,1,5)
        grid.addWidget(self.PBStart,0,6,1,1)
        grid.addWidget(self.PBnextpage,0,7,1,1)
        vbox=QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addWidget(self.LWweb)
 
         
        self.setLayout(vbox)
        self.CBBox.addItem("baidu")
        self.CBBox.addItem("360")
        
        
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

        self.keyword = ""
        self.page = 1
        self.ClassSearch = None
        
        
        
        
        
        self.connect(self.PBStart, SIGNAL('clicked()'), self.start)
        self.connect(self.PBnextpage, SIGNAL('clicked()'), self.nextpage)
        
    def contextMenuEvent(self, event):
        if self.LWweb.count()>0:
            self.content.exec_(QCursor.pos())
        
    def start(self):
        self.LWweb.clear()
        self.page = 1
        s = self.CBBox.currentText()
        if s == "baidu":
            self.ClassSearch = Baidu()
        elif s == "360":
            self.ClassSearch = Haosou()
        self.search()
        
    def nextpage(self):
        if self.ClassSearch:
            self.page = self.page+1
            self.search()
            
    def copy(self):
        clipboard = QApplication.clipboard()
        text = self.LWweb.currentItem().text() 
        clipboard.setText(text)
        
    def search(self):
        result=None
        self.keyword = self.LEkeyword.text()
        keyword = unicode(self.keyword)
        if keyword:
            result = self.ClassSearch.search(keyword, self.page)

        if result:
            self.addUrl(result)
            
    def addUrl(self, result):
        for name, url in result:
            item = QListWidgetItem()
            item.setText(url)
            item.setToolTip(name)
            self.LWweb.addItem(item)
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
    form = UrlGet()
    form.show()
    sys.exit(app.exec_())