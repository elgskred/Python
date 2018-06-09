from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QToolTip, QMessageBox, QWidget, QAction, QTabWidget,QVBoxLayout, QBoxLayout, QFormLayout, QLabel, QScrollArea, QScrollBar, QInputDialog, QLineEdit, QFileDialog, QGridLayout
from PyQt5.QtCore import QCoreApplication, QRect, pyqtSlot
from PyQt5.QtGui import QIcon, QFont
import main
import operator


import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.title = 'Placeholder'
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        
        #button = QPushButton('Close', self)
        #button.move(400,100)
        #button.clicked.connect(self.CloseApp)

        self.InitWindow()
        
        
        
    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        self.quit = QAction("Quit", self)
        self.quit.triggered.connect(self.closeEvent)
        
        self.show()
        
    def Close_Clicked(self):
        QCoreApplication.instance().quit()
    
    def CloseApp(self):
        reply = QMessageBox.question(self, "Close message", "Exit the application?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
    
    def closeEvent(self, event):
        print("Close")

class MyTableWidget(QWidget):        
 
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        #Fonts
        boldFont = QFont()
        boldFont.setBold(True)
 
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QScrollArea()
        self.tab3 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1,"Statistics")
        self.tabs.addTab(self.tab2,"Tab 2")
        self.tabs.addTab(self.tab3, "Settings")
 
        #Create Statistics tab with content
        self.tab1.layout = QGridLayout(self)
        if not main.CheckIfSaveExists():
            if main.CreateEmptyDataStructure():
                print('Savefile created')
                self.dataStruct = main.OpenDataStructure()
            else:
                print('Something went wrong when creating a empty savefile')
        else:
            self.dataStruct = main.OpenDataStructure()  
        sorted_totalStats = sorted(self.dataStruct['totalStats'].items(),key=lambda x:operator.getitem(x[1],'count'), reverse=True)
        
#        for inst in sorted_totalStats:
#            print(inst)
#            print(inst[0])
#            print(inst[1]['count'])
            
        
        
        
    
    
    
    
    
    
    
    
    
    
        # Create first tab
#        self.tab1.layout = QFormLayout(self)
#        self.pushButton1 = QPushButton("PyQt5 button")
#        self.pushButton2 = QPushButton("PyQt5 button")
#        self.label1 = QLabel('Test', self)
#        #self.tab1.layout.addWidget(self.pushButton1)
#        #self.tab1.layout.addWidget(self.pushButton2)
#        self.tab1.layout.addRow(self.label1, self.pushButton1)
#        #self.tab1.layout.addRow(self.pushButton1, self.pushButton2)
#        self.tab1.setLayout(self.tab1.layout)
#        self.tab1.move(100, 100)
        
        # Create second tab
        self.content_widget = QWidget()
        self.tab2.setWidget(self.content_widget)
        self.flay = QGridLayout(self.content_widget)
        self.tab2.setWidgetResizable(True)
        
        self.leftColumn = QLabel('Instance Name:', self)
        self.leftColumn.setFont(boldFont)
        self.middleColumn = QLabel('Instance Count:', self)
        self.middleColumn.setFont(boldFont)
        self.rightColumn = QLabel('Avg Time in Instance(secs):', self)
        self.rightColumn.setFont(boldFont)
        self.flay.addWidget(self.leftColumn, 0, 0)
        self.flay.addWidget(self.middleColumn, 0, 1)
        self.flay.addWidget(self.rightColumn, 0, 2)
        
        
        cnt = 1
        for inst in sorted_totalStats:
            print(inst)
            self.labelLeft = QLabel(str(inst[0]), self)
            self.labelMiddle = QLabel(str(inst[1]['count']), self)
            self.labelRight = QLabel(str(inst[1]['avgTime']), self)
            
            self.flay.addWidget(self.labelLeft, cnt,0)
            self.flay.addWidget(self.labelMiddle, cnt,1)
            self.flay.addWidget(self.labelRight, cnt,2)
            cnt += 1
            
            
        
#        self.t1 = QLabel('Test1', self)
#        self.t2 = QLabel('Test2', self)
#        self.t3 = QLabel('Test3', self)
#        self.t4 = QLabel('Test4', self)
#        self.t5 = QLabel('Test5', self)
#        self.t6 = QLabel('Test6', self)
#        self.flay.addRow(self.t1)
#        self.flay.addRow(self.t2)
#        self.flay.addRow(self.t3)
#        self.flay.addRow(self.t4)
#        self.flay.addRow(self.t5)
#        self.flay.addRow(self.t6)
        #self.tab2.setLayout(self.tab2.layout)
        
        
        #Create third tab
        self.tab3.layout = QGridLayout(self)
        self.textbox = QLineEdit(self)
        self.textbox.resize(50, 40)
        self.pathLabel = QLabel('Client.txt location', self)
        self.browseButton = QPushButton('Browse')
        self.browseButton.clicked.connect(self.on_click)
        
        self.tab3.layout.addWidget(self.pathLabel, 0, 0)
        self.tab3.layout.addWidget(self.textbox, 0, 1)
        self.tab3.layout.addWidget(self.browseButton, 0, 2)
        self.tab3.setLayout(self.tab3.layout)
        
        
        
        # Add tabs to widget        
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.tabs.resize(300,100)
        #self.tabs.setMaximumWidth(300)
        #self.tabs.setMaximumHeight(100)


    @pyqtSlot()
    def on_click(self):
        print("Button click")
        self.t = Filedialog()
        self.textbox.setText(self.t.path)

        
class Filedialog(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.openFileNameDialog()
 
    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            self.path = fileName



        



#App = QApplication(sys.argv)
App = QCoreApplication.instance()
if App is None:
    App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())




