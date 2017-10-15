from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QInputDialog, QLineEdit, QFileDialog, QCheckBox, QButtonGroup, QMessageBox
from PyQt5.QtGui import QIcon, QDoubleValidator
from PyQt5 import QtCore
import sys
import cctbx
import numpy as np
import os
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
		self.resolution = 1
		self.scaling_factor = 1
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
		self.mtz_name, _ = QFileDialog.getOpenFileName(self,"Chooose an MTZ file", "","All Files (*);;MTZ Files (*.mtz)", options=options)
		self.textbox1.setText(self.mtz_name)
		msgBox = QMessageBox()
		msgBox.setText("Successfully found MTZ file.")
		msgBox.setWindowTitle("MTZ File")
		msgBox.exec_()

	def mtz_text_editor_enter(self):
		tmp = self.textbox1.text()
		if os.path.isfile(tmp):
			self.mtz_name = tmp
			msgBox = QMessageBox()
			msgBox.setText("Successfully found MTZ file.")
			msgBox.setWindowTitle("MTZ File")
			msgBox.exec_()
	def show_mtz(self):
		pass
	
	#Operations about PDB file
	def load_pdb(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		self.pdb_name, _ = QFileDialog.getOpenFileName(self,"Choose a PDB file", "","All Files (*);;PDB Files (*.pdb)", options=options)
		self.textbox2.setText(self.pdb_name)
		msgBox = QMessageBox()
		msgBox.setText("Successfully found PDB file.")
		msgBox.setWindowTitle("PDB File")
		msgBox.exec_()
	def pdb_text_editor_enter(self):
		tmp = self.textbox2.text()
		if os.path.isfile(tmp):
			self.pdb_name = tmp
			msgBox = QMessageBox()
			msgBox.setText("Successfully found PDB file.")
			msgBox.setWindowTitle("PDB File")
	def show_pdb(self):
		pass
		
	#Operations about FCF file
	def load_fcf(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		self.fcf_name, _ = QFileDialog.getOpenFileName(self,"Choose an FCF file", "","All Files (*);;FCF Files (*.fcf)", options=options)
		self.textbox3.setText(self.fcf_name)
		msgBox = QMessageBox()
		msgBox.setText("Successfully found FCF file.")
		msgBox.setWindowTitle("FCF File")
		msgBox.exec_()
	def fcf_text_editor_enter(self):
		tmp = self.textbox3.text()
		if os.path.isfile(tmp):
			self.fcf_name = tmp
			msgBox = QMessageBox()
			msgBox.setText("Successfully found FCF file.")
			msgBox.setWindowTitle("FCF File")
	def show_fcf(self):
		pass
		
	#Operations about CIF file
	def load_cif(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		self.cif_name, _ = QFileDialog.getOpenFileName(self,"Choose a CIF file", "","All Files (*);;CIF Files (*.cif)", options=options)
		self.textbox4.setText(self.cif_name)
		msgBox = QMessageBox()
		msgBox.setText("Successfully found CIF file.")
		msgBox.setWindowTitle("CIF File")
		msgBox.exec_()
	def cif_text_editor_enter(self):
		tmp = self.textbox4.text()
		if os.path.isfile(tmp):
			self.cif_name = tmp
			msgBox = QMessageBox()
			msgBox.setText("Successfully found CIF file.")
			msgBox.setWindowTitle("CIF File")
	def show_cif(self):
		pass
		
	#Set resolution
	def set_resolution(self):
		self.resolution = float(self.textbox5.text())
		msgBox = QMessageBox()
		msgBox.setText("Successfully set the resolution to {}".format(self.resolution))
		msgBox.setWindowTitle("Resolution")
		msgBox.exec_()
		
	def set_wilson_scaling_factor(self):
		self.scaling_factor = float(self.textbox6.text())
		msgBox = QMessageBox()
		msgBox.setText("Successfully set scaling factor to {}".format(self.scaling_factor))
		msgBox.setWindowTitle("Scaling Factor")
		msgBox.exec_()
		
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
		self.cb1.toggle()
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
		btn6 = QPushButton("Set Resolution", self)
		btn6.move(75, 230)
		btn6.resize(100, 35)
		btn6.clicked.connect(self.set_resolution)
		
		#Overall wilson plot scaling factor
		self.textbox6 = QLineEdit(self)
		self.textbox6.move(10, 270)
		self.textbox6.resize(60, 35)
		self.textbox6.setValidator(QDoubleValidator(self,bottom=-500,top=500,decimals=4))
		btn6 = QPushButton("Set Wilson\nFactor", self)
		btn6.move(75, 270)
		btn6.resize(100, 35)
		btn6.clicked.connect(self.set_wilson_scaling_factor)
		
	def plot_Fcalc_Fobs(self):
		if self.cb1_1.checkState():#1 get Fobs from mtz file
			mtz_file = read_mtz(self.mtz_name)
			Fobs = mtz_file.as_miller_arrays()[2]
			Fobs_DF = pd.DataFrame(index=pd.MultiIndex.from_tuples(Fobs.indices()),\
								data=np.array(Fobs.data()*self.scaling_factor))

		elif self.cb2_1.checkState():#2 get Fobs from fcf file
			fcf_file = read_fcf(self.fcf_name)
		
		#-------------------------------------------------------------------------------
		if self.cb1.checkState():#1 get Fcalc by calculating the structure factor from pdb file
			pdb_structure = read_pdb(self.pdb_name)
			Fcalc = calc_structure_factors(pdb_structure,dmin=self.resolution)
			Fcalc_data = Fcalc.data()
			Fcalc_indices = Fcalc.indices()
			Fcalc_DF = pd.DataFrame(index=pd.MultiIndex.from_tuples(Fcalc_indices),data=np.abs(Fcalc_data))
			
		elif self.cb2.checkState():#2 get Fcalc by calculating the structure factor from cif file
			cif_structures = read_cif(self.cif_name)
			for name, cif_structure in cif_sturctures.items():
				Fcalc = f_calc_structure_factors(cif_structure,dmin=self.resolution,scatfact_table='electron',\
											return_as="miller",verbose=True)
				break #abandon any more structures in the cif file, if there is any, only read the first one
			Fcalc_data = Fcalc.data()
			Fcalc_indices = Fcalc.indices()
			Fcalc_DF = pd.DataFrame(index=pd.MultiIndex.from_tuples(Fcalc_indices),data=np.abs(Fcalc_data))
			
		elif self.cb3.checkState():#3 get Fcalc from mtz file
			if not self.cb1_1.checkState():
				mtz_file = read_mtz(self.mtz_name)
			Fcalc = mtz_file.as_miller_arrays()[3]
			Fcalc_DF = pd.DataFrame(index=pd.MultiIndex.from_tuples(Fcalc.indices()),data=np.abs(Fcalc.data()))

		elif self.cb4.checkState():#4 get Fcalc from fcf file
			if not self.cb2_1.checkState():
				fcf_file = read_fcf(self.fcf_name)
				
		merged_x = []
		merged_y = []
		for i in Fobs.indices():
			merged_x.append(Fobs_DF.loc[i][0])
			merged_y.append(Fcalc_DF.loc[i][0])
			
		plt.figure()
		x2, y2 = pd.Series(merged_x, name="F_obs"), pd.Series(merged_y, name="F_model")
		ax = sns.regplot(x=x2, y=y2, marker='+')
		plt.show()
			
def read_pdb(f):
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
	
def read_cif(f):
	#read a cif file  One cif file can contain multiple structures
	try:
		if isinstance(f,str):
			structures=cif.reader(file_name=f,raise_sorry_if_format_error=True).build_crystal_structures()
		else:
			raise TypeError,'read_cif: Cannot deal is type {}'.format(type(f))
	except libtbx.utils.Sorry as e:
		print e
		print "Error parsing cif file, check if the data tag does not contain any spaces."
		exit()
	return structures
	
def read_mtz(f):
	#read an mtz file
	return any_reflection_file(str(f))
	
def read_fcf(f):
	#read an fcf file
	pass

def f_calc_structure_factors(structure,**kwargs):
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
        
def calc_structure_factors(structures,dmin=1.0,table='electron',prefix='',verbose=True,**kwargs):
    """Wrapper around f_calc_structure_factors()
    Takes a structure object in which there is only one strcture

    dmin can be a dataframe and it will take the minimum dspacing (as specified by col 'd') or a float
    if combine is specified, function will return a dataframe combined with the given one, otherwise a
    dictionary of dataframes

    prefix is a prefix for the default names fcalc/phases to identify different structures
    """    
    fcalc = f_calc_structure_factors(structures,dmin=dmin,scatfact_table=table,\
                                    return_as="miller",verbose=verbose,**kwargs)

    return fcalc
	
		
if __name__ == "__main__":
	app = QApplication(sys.argv)
	ex = Main_Window()
	sys.exit(app.exec_())