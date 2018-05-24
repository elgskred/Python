from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QToolTip, QMessageBox
from PyQt5.QtCore import QCoreApplication
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.title = 'Placeholder'
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        
        button = QPushButton('Close', self)
        button.move(200,200)
        #button.clicked.connect(self.close)
        button.clicked.connect(self.CloseApp)
        
        self.InitWindow()
        
    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()
        
    def Close_Clicked(self):
        QCoreApplication.instance().quit()
    
    def CloseApp(self):
        reply = QMessageBox.question(self, "Close message", "Exit the application?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

#App = QApplication(sys.argv)
App = QCoreApplication.instance()
if App is None:
    App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())