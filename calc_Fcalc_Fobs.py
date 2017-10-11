import cctbx
import numpy as np
import os
import pandas as pd
import iotbx.pdb as pdb
import scitbx
import libtbx.utils
import matplotlib.pyplot as plt
from iotbx.reflection_file_reader import any_reflection_file
import seaborn as sns; sns.set(color_codes=True)
from scipy.stats import spearmanr, pearsonr, linregress

def read_pdb(f):
    """read a pdb file"""
    try:
        if isinstance(f,str):
            structures=pdb.input(file_name=f,raise_sorry_if_format_error=True).xray_structure_simple()
        else:
            raise TypeError,'read_pdb: Cannot deal is type {}'.format(type(f))
    except libtbx.utils.Sorry as e:
        print e
        print "Error parsing cif file, check if the data tag does not contain any spaces."
        exit()
    return structures
	
	
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
	PDB_file_name = {'1':'EMX_Lysozyme2_refine_096_1dataset.pdb','4':'EMX_Lysozyme2_refine_084_H2oOK_4datasets.pdb',\
					'10_best':'EMX_Lysozyme2_refine_160_10best.pdb','10_random':'EMX_Lysozyme2_refine_161_10random.pdb',\
					'20_best':'EMX_Lysozyme2_refine_162_20best.pdb','33':'EMX_Lysozyme_refine39_33crystaldataset.pdb',\
					'1_refine':'EMX_Lysozyme2_refine_096_1dataset.pdb','33_refine':'EMX_Lysozyme_refine39_33crystaldataset.pdb',\
					'10_random_refine':'EMX_Lysozyme2_refine_161_10random.pdb'}
	Merged_ref_file_name = {'1':'data_NL_0213-10_test01_P21212_CCP4_I+F_1dataset.mtz','4':'partial_merge_test03_P21212_CCP4_I+F_4datasets.mtz',\
							'10_best':'10best_datasets_merge_test02_P21212_CCP4_I+F.mtz','10_random':'10random_datasets_merge_test01_P21212_CCP4_I+F.mtz',\
							'20_best':'20best_datasets_merge_test02_P21212_CCP4_I+F.mtz','33':'all_datasets_merge_test03_P21212_CCP4_I+F.mtz',\
							'1_refine':'EMX_Lysozyme2_refine_096_1dataset.mtz','33_refine':'EMX_Lysozyme2_refine_039_alldatasets.mtz',\
							'4_refine':'EMX_Lysozyme2_refine_084_4datasets.mtz','10_best_refine':'EMX_Lysozyme2_refine_160_10best.mtz', \
							'10_random_refine':'EMX_Lysozyme2_refine_161_10random.mtz', '20_best_refine':'EMX_Lysozyme2_refine_162_20best.mtz',\
							'1_xscale':'data_NL_0213-10_test01_P21212_XSCALE_CCP4_I+F_1dataset.mtz'}

	k_overall = {'1_refine': 0.9167, '4_refine': 0.9581, '10_best_refine':0.9167, '10_random_refine':0.9167, '20_best_refine':0.9549, '33_refine': 0.9549}
#	lysozyme = read_pdb(PDB_file_name['1'])
#	F_lysozyme = calc_structure_factors(lysozyme,dmin=2.19)
#	F_data = F_lysozyme.data()
#	indices = F_lysozyme.indices()
#	intensity = np.power(np.abs(F_data),2)
#	intensity_lysozyme = pd.DataFrame(index=pd.MultiIndex.from_tuples(indices),data=intensity)

	
	merged_hkl_file = any_reflection_file(Merged_ref_file_name['4_refine'])
#	merged_miller_array = merged_hkl_file.as_miller_arrays()[0]
#	merged_indices = merged_miller_array.indices()
#	merged_intensity = merged_miller_array.data()
#	merged_intensity_lysozyme = pd.DataFrame(index=pd.MultiIndex.from_tuples(merged_indices),data=np.array(merged_intensity))
#	merged_x = []
#	merged_y = []
#	for i in merged_indices:
#		merged_x.append(merged_intensity_lysozyme.loc[i][0])
#		merged_y.append(intensity_lysozyme.loc[i][0])
#
#	plt.figure()
#	x2, y2 = pd.Series(merged_x, name="Iobs"), pd.Series(merged_y, name="Fcalc^2")
#	ax = sns.regplot(x=x2, y=y2, marker='+')
#	plt.show()
	
	merged_miller_array = merged_hkl_file.as_miller_arrays()[3]
	F_data = merged_miller_array.data()
	indices = merged_miller_array.indices()
	merged_miller_array = merged_hkl_file.as_miller_arrays()[2]
	merged_Fobs = merged_miller_array.data()
	merged_indices = merged_miller_array.indices()
	Fcalc_lysozyme = pd.DataFrame(index=pd.MultiIndex.from_tuples(indices),data=np.abs(F_data))
	merged_Fobs_lysozyme = pd.DataFrame(index=pd.MultiIndex.from_tuples(merged_indices),data=np.array(merged_Fobs)*k_overall['4_refine'])
	merged_x = []
	merged_y = []
	for i in merged_indices:
		merged_x.append(merged_Fobs_lysozyme.loc[i][0])
		merged_y.append(Fcalc_lysozyme.loc[i][0])
    
	plt.figure()
	x2, y2 = pd.Series(merged_x, name="F_obs"), pd.Series(merged_y, name="F_model")
	ax = sns.regplot(x=x2, y=y2, marker='+')
	plt.show()
	line = ax.get_lines()[0]
	slope, intercept, r_value, p_value, std_err = linregress(x=line.get_xdata(),y=line.get_ydata())
	print 'slope: {}, intercept: {}, r_value: {}'.format(slope, intercept, r_value)
	
	print 'Spearman correlation coefficient: {}'.format(spearmanr(x2,y2))
	print 'Pearson correlation coefficient: {}'.format(pearsonr(x2,y2))
	
#	plt.figure()
#	ax = sns.regplot(x=x2, y=y2, marker='+',robust=True)
#	plt.show()
#	line = ax.get_lines()[0]
#	slope, intercept, r_value, p_value, std_err = linregress(x=line.get_xdata(),y=line.get_ydata())
#	print 'slope: {}, intercept: {}, r_value: {}'.format(slope, intercept, r_value)