# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 14:00:27 2017

@author: Taimin Yang
"""

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QInputDialog, QLineEdit, QFileDialog, QCheckBox, QButtonGroup, QMessageBox, QComboBox 
from PyQt5.QtGui import QIcon, QDoubleValidator
from PyQt5 import QtCore
import sys, traceback, os
import json
import cctbx
import numpy as np
import pandas as pd
import iotbx.pdb as pdb
import iotbx.cif as cif
import libtbx.utils
import matplotlib.pyplot as plt
from iotbx.reflection_file_reader import any_reflection_file
import seaborn as sns; sns.set(color_codes=True)

class Main_Window(QMainWindow):
    
	def __init__(self):
		super(Main_Window,self).__init__()
		self.mtz_name = ""
		self.pdb_name = ""
		self.fcf_name = ""
		self.cif_name = ""
		self.saved_Data = {}
		self.resolution = 1.8
		self.scaling_factor = 1
		self.scatfact_table = 'electron'
		self.initUI()
		self.home()
		self.show()
		
	def initUI(self):
		self.setGeometry(300, 300, 600, 400)
		self.setFixedSize(self.size())
		self.setWindowTitle('Plot_Fcalc_Fobs')
		self.setWindowIcon(QIcon('gear-tools.png'))  
		self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

	#Operations about MTZ file
	def load_mtz(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		self.mtz_name, _ = QFileDialog.getOpenFileName(self,"Chooose an MTZ file", "","MTZ Files (*.mtz);;All Files (*)", options=options)
		self.textbox1.setText(self.mtz_name)
	def mtz_text_editor_enter(self):
		tmp = self.textbox1.text()
		if os.path.isfile(tmp):
			self.mtz_name = tmp
			msgBox = QMessageBox()
			msgBox.setText("Successfully found MTZ file.")
			msgBox.setWindowTitle("MTZ File")
			msgBox.exec_()
		else:
			msgBox = QMessageBox()
			msgBox.setText("File does not exist, please enter another name")
			msgBox.setWindowTitle("File")
			msgBox.exec_()
	def read_mtz(self,f):
		#read an mtz file
		return any_reflection_file(str(f))
	def show_mtz(self):
		#try:
		self.F_Window = File_Window(str(self.mtz_name))
		#except:
		#	msgBox = QMessageBox()
		#	msgBox.setText("Failed to show MTZ file. \nPlease check if your path is right.")
		#	msgBox.setWindowTitle("MTZ File")
		#	msgBox.exec_()
	
	#Operations about PDB file
	def load_pdb(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		self.pdb_name, _ = QFileDialog.getOpenFileName(self,"Choose a PDB file", "","PDB Files (*.pdb);;All Files (*)", options=options)
		self.textbox2.setText(self.pdb_name)
	def pdb_text_editor_enter(self):
		tmp = self.textbox2.text()
		if os.path.isfile(tmp):
			self.pdb_name = tmp
			msgBox = QMessageBox()
			msgBox.setText("Successfully found PDB file.")
			msgBox.setWindowTitle("PDB File")
		else:
			msgBox = QMessageBox()
			msgBox.setText("File does not exist, please enter another name")
			msgBox.setWindowTitle("File")
			msgBox.exec_()
	def read_pdb(self,f):
		#read a pdb file
		try:
			if isinstance(f,str):
				structures=pdb.input(file_name=f,raise_sorry_if_format_error=True).xray_structure_simple()
			else:
				raise TypeError,'read_pdb: Cannot deal is type {}'.format(type(f))
		except libtbx.utils.Sorry as e:
			print e
			print "Error parsing pdb file, check if the data tag does not contain any spaces."
			exit()
		return structures
	def show_pdb(self):
		pass
		
	#Operations about FCF file
	def load_fcf(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		self.fcf_name, _ = QFileDialog.getOpenFileName(self,"Choose an FCF file", "","FCF Files (*.fcf);;All Files (*)", options=options)
		self.textbox3.setText(self.fcf_name)
	def fcf_text_editor_enter(self):
		tmp = self.textbox3.text()
		if os.path.isfile(tmp):
			self.fcf_name = tmp
			msgBox = QMessageBox()
			msgBox.setText("Successfully found FCF file.")
			msgBox.setWindowTitle("FCF File")
		else:
			msgBox = QMessageBox()
			msgBox.setText("File does not exist, please enter another name")
			msgBox.setWindowTitle("File")
			msgBox.exec_()
	def read_fcf(self,f):
		#read an fcf file
		return any_reflection_file(str(f))
	def show_fcf(f):
		pass
		
	#Operations about CIF file
	def load_cif(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		self.cif_name, _ = QFileDialog.getOpenFileName(self,"Choose a CIF file", "","CIF Files (*.cif);;All Files (*)", options=options)
		self.textbox4.setText(self.cif_name)
	def cif_text_editor_enter(self):
		tmp = self.textbox4.text()
		if os.path.isfile(tmp):
			self.cif_name = tmp
			msgBox = QMessageBox()
			msgBox.setText("Successfully found CIF file.")
			msgBox.setWindowTitle("CIF File")
		else:
			msgBox = QMessageBox()
			msgBox.setText("File does not exist, please enter another name")
			msgBox.setWindowTitle("File")
			msgBox.exec_()
	def read_cif(self,f):
		#read a cif file  One cif file can contain multiple structures
		try:
			if isinstance(f,str):
				structures=cif.reader(file_path=f,raise_if_errors=True).build_crystal_structures()
			else:
				raise TypeError,'read_cif: Cannot deal is type {}'.format(type(f))
		except libtbx.utils.Sorry as e:
			print e
			print "Error parsing cif file, check if the data tag does not contain any spaces."
			exit()
		return structures
	def show_cif(self):
		pass
		
	#Set resolution
	def set_resolution(self):
		try:
			self.resolution = float(self.textbox5.text())
			msgBox = QMessageBox()
			msgBox.setText("Successfully set the resolution to {}".format(self.resolution))
			msgBox.setWindowTitle("Resolution")
			msgBox.exec_()
		except:
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Critical)
			msgBox.setText("An Error Has Ocurred while trying to set resolution! Please check if you input the proper number.")
			msgBox.setWindowTitle("Error")
			msgBox.exec_()
			
	def set_wilson_scaling_factor(self):
		try:
			self.scaling_factor = float(self.textbox6.text())
			msgBox = QMessageBox()
			msgBox.setText("Successfully set scaling factor to {}".format(self.scaling_factor))
			msgBox.setWindowTitle("Scaling Factor")
			msgBox.exec_()
		except:
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Critical)
			msgBox.setText("An Error Has Ocurred while trying to set the wilson scaling factor! Please check if you input the proper number.")
			msgBox.setWindowTitle("Error")
			msgBox.exec_()
	
	def save_fobs_fcalc(self):
		try:
			options = QFileDialog.Options()
			options |= QFileDialog.DontUseNativeDialog
			save_name, _ = QFileDialog.getSaveFileName(self,"Save Fobs Fcalc", "","JSON Files (*.json);;All Files (*)", 										options=options)
			with open(save_name,'w') as fp:
				json.dump(self.saved_Data,fp,indent=4)
		except:
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Critical)
			msgBox.setText("An Error Has Ocurred while trying to save fobs and fcalc!")
			msgBox.setWindowTitle("Error")
			msgBox.exec_()
			
	def f_calc_structure_factors(self,structure,**kwargs):
		"""Takes cctbx structure and returns f_calc miller array
		Takes an optional options dictionary with keys:
		input:
			**kwargs:
				'd_min': minimum d-spacing for structure factor calculation
				'algorithm': which algorithm to use ('direct', 'fft', 'automatic')
			structure: <cctbx.xray.structure.structure object>
		output:
			f_calc: <cctbx.miller.array object> with calculated structure factors
				in the f_calc.data() function
		
		"""
	 
		dmin        = kwargs.get('dmin',1.0)
		algorithm 	= kwargs.get('algorithm',"automatic")
		anomalous 	= kwargs.get('anomalous',False)
		table 		= kwargs.get('scatfact_table','wk1995')
		return_as   = kwargs.get('return_as',"series")
		verbose     = kwargs.get('verbose', False)

		if dmin <= 0.0:
			raise ValueError, "d-spacing must be greater than zero."

		if algorithm == "automatic":
			if structure.scatterers().size() <= 100:
				algorithm = "direct"
			else:
				algorithm = None

		structure.scattering_type_registry(table=table)

		f_calc_manager = structure.structure_factors(
				anomalous_flag = anomalous,
				d_min = dmin,
				algorithm = algorithm)
		f_calc = f_calc_manager.f_calc()
		
		if verbose:
			print "\nScattering table:", structure.scattering_type_registry_params.table
			structure.scattering_type_registry().show()
		print "Minimum d-spacing: %g" % f_calc.d_min()

		if return_as == "miller":
			return f_calc
		elif return_as == "series":
			fcalc = pd.Series(index=f_calc.indices(),data=np.abs(f_calc.data()))
			phase = pd.Series(index=f_calc.indices(),data=np.angle(f_calc.data()))
			return fcalc,phase
		elif return_as == "df":
			dffcal = pd.DataFrame(index=f_calc.index)
			dffcal['fcalc'] = np.abs(f_calc.data())
			dffcal['phase'] = np.angle(f_calc.data())
			return dffcal
		else:
			raise ValueError, "Unknown argument for 'return_as':{}".format(return_as)
			
	def calc_structure_factors(self,structures,dmin=1.0,table='electron',prefix='',verbose=True,**kwargs):
		"""Wrapper around f_calc_structure_factors()
		Takes a structure object in which there is only one strcture

		dmin can be a dataframe and it will take the minimum dspacing (as specified by col 'd') or a float
		if combine is specified, function will return a dataframe combined with the given one, otherwise a
		dictionary of dataframes

		prefix is a prefix for the default names fcalc/phases to identify different structures
		"""    
		fcalc = self.f_calc_structure_factors(structures,dmin=dmin,scatfact_table=table,\
										return_as="miller",verbose=verbose,**kwargs)

		return fcalc
	
	def home(self):
		#quit button
		btn1 = QPushButton("Quit", self)
		btn1.clicked.connect(QtCore.QCoreApplication.instance().quit)
		btn1.resize(100, 50)
		btn1.move(490, 340)
		#plot button
		btn2 = QPushButton("Plot", self)
		btn2.clicked.connect(self.plot_Fcalc_Fobs)
		btn2.resize(100, 50)
		btn2.move(380, 340)
		
		#load mtz file button
		btn3 = QPushButton("Choose MTZ", self)
		btn3.clicked.connect(self.load_mtz)
		btn3.resize(100, 35)
		btn3.move(490, 5)
		#show the mtz file button
		btn3_1 = QPushButton("Show MTZ", self)
		btn3_1.clicked.connect(self.show_mtz)
		btn3_1.resize(100, 35)
		btn3_1.move(385, 5)
		#show the path of the mtz file
		self.textbox1 = QLineEdit(self)
		self.textbox1.resize(375, 35)
		self.textbox1.move(5, 5)
		self.textbox1.setText(self.mtz_name)
		self.textbox1.returnPressed.connect(self.mtz_text_editor_enter)
		
		#load pdb file button
		btn4 = QPushButton("Choose PDB", self)
		btn4.clicked.connect(self.load_pdb)
		btn4.resize(100, 35)
		btn4.move(490, 45)
		#show the pdb file button
		btn4_1 = QPushButton("Show PDB", self)
		btn4_1.clicked.connect(self.show_pdb)
		btn4_1.resize(100, 35)
		btn4_1.move(385, 45)
		#show the path of the pdb file
		self.textbox2 = QLineEdit(self)
		self.textbox2.resize(375, 35)
		self.textbox2.move(5, 45)
		self.textbox2.setText(self.pdb_name)
		self.textbox2.returnPressed.connect(self.pdb_text_editor_enter)
		
		#load fcf file button
		btn5 = QPushButton("Choose FCF", self)
		btn5.clicked.connect(self.load_fcf)
		btn5.resize(100, 35)
		btn5.move(490, 85)
		#show the fcf file button
		btn5_1 = QPushButton("Show FCF", self)
		btn5_1.clicked.connect(self.show_fcf)
		btn5_1.resize(100, 35)
		btn5_1.move(385, 85)
		#show the path of the fcf file
		self.textbox3 = QLineEdit(self)
		self.textbox3.resize(375, 35)
		self.textbox3.move(5, 85)
		self.textbox3.setText(self.fcf_name)
		self.textbox3.returnPressed.connect(self.fcf_text_editor_enter)
		
		#load cif file button
		btn6 = QPushButton("Choose CIF", self)
		btn6.clicked.connect(self.load_cif)
		btn6.resize(100, 35)
		btn6.move(490, 125)
		#show the cif file button
		btn6_1 = QPushButton("Show CIF", self)
		btn6_1.clicked.connect(self.show_cif)
		btn6_1.resize(100, 35)
		btn6_1.move(385, 125)
		#show the path of the cif file
		self.textbox4 = QLineEdit(self)
		self.textbox4.resize(375, 35)
		self.textbox4.move(5, 125)
		self.textbox4.setText(self.cif_name)
		self.textbox4.returnPressed.connect(self.cif_text_editor_enter)
		
		#checkbox to choose the way to calculate Fcalc
		#1 get Fcalc by calculating the structure factor from pdb file
		self.cb1 = QCheckBox('Calc Fcalc from PDB', self)
		self.cb1.move(10, 170)
		self.cb1.resize(145, 20)
		self.cb1.setAutoExclusive(1)
		#2 get Fcalc by calculating the structure factor from cif file
		self.cb2 = QCheckBox('Calc Fcalc from CIF', self)
		self.cb2.move(160, 170)
		self.cb2.resize(145, 20)
		self.cb2.setAutoExclusive(1)
		#3 get Fcalc from mtz file
		self.cb3 = QCheckBox('Get Fcalc from MTZ', self)
		self.cb3.move(305, 170)
		self.cb3.resize(145, 20)
		self.cb3.toggle()
		self.cb3.setAutoExclusive(1)
		#4 get Fcalc from fcf file
		self.cb4 = QCheckBox('Get Fcalc from FCF', self)
		self.cb4.move(455, 170)
		self.cb4.resize(145, 20)
		self.cb4.setAutoExclusive(1)
		#set a checkbox group to group the options for fobs
		self.cb_group_fcalc = QButtonGroup(self)
		self.cb_group_fcalc.addButton(self.cb1)
		self.cb_group_fcalc.addButton(self.cb2)
		self.cb_group_fcalc.addButton(self.cb3)
		self.cb_group_fcalc.addButton(self.cb4)
		self.cb_group_fcalc.setExclusive(1)
		
		#checkbox to choose the way to get Fobs
		#1 get Fobs from mtz file
		self.cb1_1 = QCheckBox('Get Fobs from MTZ', self)
		self.cb1_1.move(10, 200)
		self.cb1_1.resize(145, 20)
		self.cb1_1.toggle()
		#2 get Fobs from fcf file
		self.cb2_1 = QCheckBox('Get Fobs from FCF', self)
		self.cb2_1.move(160, 200)
		self.cb2_1.resize(145, 20)
		#set a checkbox group to group the options for fobs
		self.cb_group_fobs = QButtonGroup(self)
		self.cb_group_fobs.addButton(self.cb1_1)
		self.cb_group_fobs.addButton(self.cb2_1)
		self.cb_group_fobs.setExclusive(1)
		
		#input textbox to set resolution
		self.textbox5 = QLineEdit(self)
		self.textbox5.move(10, 230)
		self.textbox5.resize(60, 35)
		self.textbox5.setValidator(QDoubleValidator(self,bottom=0,top=500,decimals=2))
		self.textbox5.setText(str(self.resolution))
		btn7 = QPushButton("Set Resolution", self)
		btn7.move(75, 230)
		btn7.resize(100, 35)
		btn7.clicked.connect(self.set_resolution)
		
		#Overall wilson plot scaling factor
		self.textbox6 = QLineEdit(self)
		self.textbox6.move(10, 270)
		self.textbox6.resize(60, 36)
		self.textbox6.setValidator(QDoubleValidator(self,bottom=-500,top=500,decimals=4))
		self.textbox6.setText(str(self.scaling_factor))
		btn8 = QPushButton("Set Wilson\nFactor", self)
		btn8.move(75, 270)
		btn8.resize(100, 36)
		btn8.clicked.connect(self.set_wilson_scaling_factor)
		
		#Save the Fobs and Fcalc as text file
		btn9 = QPushButton("Save", self)
		btn9.move(270, 340)
		btn9.resize(100, 50)
		btn9.clicked.connect(self.save_fobs_fcalc)
		
		#Combobox to select scattering factors
		self.combo = QComboBox(self)
		self.combo.addItem('electron','electron')
		self.combo.addItem('xray-wk1995','wk1995')
		self.combo.addItem('xray-it1992','it1992')
		self.combo.move(185,230)
		self.combo.resize(150,35)
		
	def plot_Fcalc_Fobs(self):
		try:
			if self.cb1_1.checkState():#1 get Fobs from mtz file
				mtz_file = self.read_mtz(self.textbox1.text())
				Fobs = mtz_file.as_miller_arrays()[2]
				Fobs_DF = pd.DataFrame(index=pd.MultiIndex.from_tuples(Fobs.indices()),\
									data=np.array(Fobs.data()*self.scaling_factor))
			elif self.cb2_1.checkState():#2 get Fobs from fcf file
				fcf_file = self.read_fcf(self.textbox3.text())
				model = dict(fcf_file.file_content().model().items()[0][1])
				if model['_shelx_refln_list_code'] is '6':
					Fobs = fcf_file.as_miller_arrays()[1] #This Fobs is Fobs^2 but in order to be more convinient for me just call it Fobs
					Fobs_DF = pd.DataFrame(index=pd.MultiIndex.from_tuples(Fobs.indices()),\
									data=np.sqrt(Fobs.data())*self.scaling_factor)
				elif model['_shelx_refln_list_code'] is '4':
					Fobs = fcf_file.as_miller_arrays()[1] #This Fobs is Fobs^2 but in order to be more convinient for me just call it Fobs
					Fobs_DF = pd.DataFrame(index=pd.MultiIndex.from_tuples(Fobs.indices()),\
									data=np.sqrt(Fobs.data())*self.scaling_factor)
				elif model['_shelx_refln_list_code'] is '3':
					Fobs = fcf_file.as_miller_arrays()[1]
					Fobs_DF = pd.DataFrame(index=pd.MultiIndex.from_tuples(Fobs.indices()),\
									data=np.array(Fobs.data())*self.scaling_factor)

		#-------------------------------------------------------------------------------
			if self.cb1.checkState():#1 get Fcalc by calculating the structure factor from pdb file
				self.scatfact_table = str(self.combo.currentData())
				pdb_structure = self.read_pdb(str(self.textbox2.text()))
				Fcalc = self.calc_structure_factors(pdb_structure,dmin=self.resolution,table=self.scatfact_table)
				Fcalc_data = Fcalc.data()
				Fcalc_indices = Fcalc.indices()
				Fcalc_DF = pd.DataFrame(index=pd.MultiIndex.from_tuples(Fcalc_indices),data=np.abs(Fcalc_data))
				
			elif self.cb2.checkState():#2 get Fcalc by calculating the structure factor from cif file
				self.scatfact_table = str(self.combo.currentData())
				cif_structures = self.read_cif(str(self.textbox4.text()))
				for name, cif_structure in cif_structures.items():
					Fcalc = self.calc_structure_factors(cif_structure,dmin=self.resolution,table=self.scatfact_table)
					break #abandon any more structures in the cif file, if there is any, only read the first one
				Fcalc_P1 = Fcalc.expand_to_p1()
				Fcalc_data = Fcalc_P1.data()
				Fcalc_indices = Fcalc_P1.indices()
				Fcalc_DF = pd.DataFrame(index=pd.MultiIndex.from_tuples(Fcalc_indices),data=np.abs(Fcalc_data))
				
			elif self.cb3.checkState():#3 get Fcalc from mtz file
				if not self.cb1_1.checkState():
					mtz_file = self.read_mtz(self.textbox1.text())
				Fcalc = mtz_file.as_miller_arrays()[3]
				Fcalc_DF = pd.DataFrame(index=pd.MultiIndex.from_tuples(Fcalc.indices()),data=np.abs(Fcalc.data()))

			elif self.cb4.checkState():#4 get Fcalc from fcf file
				if not self.cb2_1.checkState():
					fcf_file = self.read_fcf(self.textbox3.text())
					model = dict(fcf_file.file_content().model().items()[0][1])
					
				if model['_shelx_refln_list_code'] is '6':
					Fcalc = fcf_file.as_miller_arrays()[0]
					Fcalc_DF = pd.DataFrame(index=pd.MultiIndex.from_tuples(Fcalc.indices()),\
									data=np.abs(Fcalc.data())*self.scaling_factor)
				elif model['_shelx_refln_list_code'] is '4':
					Icalc = fcf_file.as_miller_arrays()[0]
					Fcalc_DF = pd.DataFrame(index=pd.MultiIndex.from_tuples(Icalc.indices()),\
									data=np.sqrt(Icalc.data())*self.scaling_factor)
				elif model['_shelx_refln_list_code'] is '3':
					Fcalc = fcf_file.as_miller_arrays()[0]
					Fcalc_DF = pd.DataFrame(index=pd.MultiIndex.from_tuples(Fcalc.indices()),\
									data=np.abs(Fcalc.data())*self.scaling_factor)
				
		#-------------------------------------------------------------------------------
			merged_x = []
			merged_y = []
			for i in Fobs.indices():
				merged_x.append(Fobs_DF.loc[i][0])
				merged_y.append(Fcalc_DF.loc[i][0])
			plt.figure()
			x2, y2 = pd.Series(merged_x, name="F_obs"), pd.Series(merged_y, name="F_model")
			self.saved_Data['Fobs'] = merged_x
			self.saved_Data['Fcalc'] = merged_y
			ax = sns.regplot(x=x2, y=y2, marker='+')
			plt.show()
			
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			tb = traceback.extract_tb(exc_tb)[0]
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Critical)
			msgBox.setText("An Error Has Ocurred!\n{}\nAt Line: {} In Function: {}".format(e.args[0], str(tb[1]), tb[2]))
			msgBox.setWindowTitle("Error")
			msgBox.exec_()
			
class File_Window(QMainWindow):
	def __init__(self,f):
		super(File_Window,self).__init__()
		self.initUI()
		self.show_file(f)
		self.show()
		
	def initUI(self):
		self.setGeometry(400, 400, 600, 800)
		self.setFixedSize(self.size())
		self.setWindowIcon(QIcon('gear-tools.png'))  
		self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
		
	def show_file(self,f):
		appendix = f.split('.')[-1].lower()
		print appendix, f
		if appendix == 'mtz':
			print f
		elif appendix == 'pdb': 
			pass
		elif appendix == 'fcf':
			pass
		elif appendix == 'cif':
			pass
		else:
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Critical)
			msgBox.setText("An Error Has Ocurred while trying to show the {} file!".format(appendix.upper()))
			msgBox.setWindowTitle("Error")
			msgBox.exec_()
		
if __name__ == "__main__":
	app = QApplication(sys.argv)
	ex = Main_Window()
	sys.exit(app.exec_())