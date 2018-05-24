from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QCoreApplication
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.title = 'Placeholder'
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 500
        
        self.InitWindow()
        
    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()
        


#App = QApplication(sys.argv)
App = QCoreApplication.instance()
if App is None:
    App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())