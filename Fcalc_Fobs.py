from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
import sys


class Main_Window(QMainWindow):
    
	def __init__(self):
		super(Main_Window,self).__init__()
		self.initUI()
		self.home()
		self.show()
        
	def initUI(self):
		self.setGeometry(300, 300, 600, 400)
		self.setWindowTitle('Plot_Fcalc_Fobs')
		self.setWindowIcon(QIcon('gear-tools.png'))        
		
	def home(self):
		#quit button
		btn1 = QPushButton("Quit", self)
		btn1.clicked.connect(QtCore.QCoreApplication.instance().quit)
		btn1.resize(100,50)
		btn1.move(490,340)
		#plot button
		btn2 = QPushButton("Plot", self)
		btn2.clicked.connect(self.plot_Fcalc_Fobs)
		btn2.resize(100,50)
		btn2.move(380,340)
		#load mtz file button
		btn3 = QPushButton("Choose MTZ", self)
		btn3.clicked.connect(self.load_mtz)
		btn3.resize(100,35)
		btn3.move(490,5)
		#load pdb file button
		btn3 = QPushButton("Choose PDB", self)
		btn3.clicked.connect(self.load_pdb)
		btn3.resize(100,35)
		btn3.move(490,45)
		
		
	def plot_Fcalc_Fobs(self):
		pass
		
	def load_mtz(self):
		pass
	
	def load_pdb(self):
		pass

if __name__ == "__main__":
	app = QApplication(sys.argv)
	ex = Main_Window()
	sys.exit(app.exec_())