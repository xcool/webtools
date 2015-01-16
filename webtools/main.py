# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from modules.UrlGet import UrlGet
from modules.SameSite import SameSite
import resource.resources

class Main_Window(QMainWindow):
    def __init__(self,parent=None):
        super(Main_Window,self).__init__(parent)
        
        self.tabWidget=QTabWidget()
        self.setCentralWidget(self.tabWidget)

    
        self.urlget=UrlGet()
        self.tabWidget.addTab(self.urlget, QString(u"爬网页"))
        self.tabWidget.setCurrentWidget(self.urlget)
        
        self.samesite=SameSite()
        self.tabWidget.addTab(self.samesite,QString(u"同站查询"))
        
        
        
        self.setWindowTitle(u"综合工具")
        self.setWindowIcon(QIcon(":/images/main.png"))
        backImg = QPixmap(":/images/background").scaled(self.size())
        self.palette = QPalette()
        self.palette.setBrush(self.backgroundRole(), QBrush(backImg))
        self.setPalette(self.palette)
        
        self.setGeometry(300,100,600,500)






        

        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Main_Window()
    form.show()
    sys.exit(app.exec_())