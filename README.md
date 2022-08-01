# SVP Additional Tools
This is collection of scripts and tests that are useful for debugging the [System Validation Platform](https://github.com/jayatsandia/svp)'s interaction with different equipment. It provides examples of interacting with equipment of the same type, e.g., communicating with multiple DER devices.  It also provides some simple examples of testing that are not included in the larger projects to create [IEEE 1547-2018](https://github.com/jayatsandia/svp_1547.1), [UL 1741](https://github.com/jayatsandia/svp_UL1741SA), and other working directories. 

## Multi-input inverter testing
The [multi_mppt_analysis.py script](/Scripts/multi_mppt_analysis.py) was used to create a model and test protocol for overall DC-to-AC power conversion efficiency for multi-input inverters.  Information on this work is at the following citations: 
*	[C. Hansen, J. Johnson, R. Darbali, N. Gurule, “Modeling Efficiency of Inverters with Multiple Inputs,” IEEE Photovoltaic Specialists Conference (PVSC), 2022.](https://www.researchgate.net/publication/361114989_Modeling_Efficiency_of_Inverters_with_Multiple_Inputs)
*	C. Hansen, J. Johnson, R. Darbali, N. Gurule, S. Gonzalez, “Test Procedure to Calculate Multi-Input Inverter Efficiency,” 8th World Conference on Photovoltaic Energy Conversion (WCPEC-8), Milan, Italy, 26-30 Sept 2022 (forthcoming). 

## Stand-alone Scripts
These are helpful native python scripts that do not rely on the SVP GUI framework to run.  They may be useful in early-stage debugging. 

# Installation
Install the SVP dependencies using this [guide](https://github.com/jayatsandia/svp/blob/master/doc/INSTALL.md).  It’s recommended to use Python 3.7.X because there were some issues reported for 3.9+. 

To run an SVP test, you will need to do the following: 
1. Copy the `Lib` directory from the svp_energy_lab into the `Lib` folder in svp_1547.1 (we decided to keep a single, separate copy of the drivers in [svp_energy_lab](https://github.com/jayatsandia/svp_energy_lab) to simplify management).  
2. Run the `ui.py` code in the opensvp to generate the GUI. 
3. Navigate to the Interoperability Test in `tests` in the left pane of the GUI, right click -> edit. 
4. Run the test and verify it works. 
