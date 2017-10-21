# Fcalc_Fobs_plot
Comparing Fcalc and Fobs of crystal structures

Compare the Fcalc and Fobs from the refinement result of Phenix and Shelxl. In MTZ file from Phenix, there are F_model and F_obs_filtered. In FCF file from SHELXL, there are Fcalc and Fobs

To use this software:
1. Install Anaconda: https://www.anaconda.com/download/ and add (PATH to Anaconda)/Script, (PATH to Anaconda), (PATH to Anaconda)/Library/bin to your $PATH
2. Install pyqt5: http://pyqt.sourceforge.net/Docs/PyQt5/installation.html or conda search pyqt and use conda install -c to install the package
3. Install DIALS or CCTBX: http://dials.lbl.gov/installation.html or http://cci.lbl.gov/cctbx_build/
4. Install seaborn, matplotlib: conda search seaborn, conda search matplotlib
5. Install CCP4 and add (PATH to CCP4)/(version)/bin to your $PATH

After Dials or CCTBX is installed, set environmental variables:
$LIBTBX_BUILD as the build folder in the dials folder and also set
PYTHONPATH=%LIBTBX_BUILD%\..\modules;%LIBTBX_BUILD%\..\modules\cctbx_project;%LIBTBX_BUILD%\..\modules\cctbx_project\boost_adaptbx;%LIBTBX_BUILD%\..\modules\cctbx_project\libtbx\pythonpath;%LIBTBX_BUILD%\lib;
This will allow you to use functions in cctbx in python