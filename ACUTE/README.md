# ACUTE: Artificially Intelligent Agent Based COVID-19 Simulation Framework

## Installing Requirements
Requirements can be installed as  
`pip3 install -r requirements.txt`  
Please note that the code has been executed and tested on Ubuntu OS, it may behave differently for any other OS  


## How to run the code

To run a sample simulation of the Islamabad, type:
`python3 run.py --location=islamabad --transition_scenario=smart-lockdown --transition_mode=1 --output_dir=output`  

To run a sample simulation of the Abbottabad, type:
`python3 run.py --location=abbottabad --transition_scenario=abbottabad-lockdown --transition_mode=1 --output_dir=output`

Running code directly from python file offer a much higher degree of control over the input paramters. You can also edit run.py file as per need and configure many other parameters for the simulation

### Running from GUI
You can also use GUI to run code. To start the UI please execute the following command.
`python3 run_wizard.py`


Outputs are written as CSV files in the output\_dir. E.g. for the islamabad run you will get:
covid\_out\_infections.csv
islamabad-smart-lockdown-27.csv


We also included a simple plotting script. This can be called e.g. as follows:
`python3 PlotSEIR.py test-extend-lockdown-62.csv test`

## Advanced usage

### Running with a specific data directory
Flacs can be run with a different input data directory as follows:
`python3 run.py --location=abbottabad --transition_scenario=extend-lockdown --transition_mode=1 --output_dir=. --data_dir=abbottabadData`

### Performing quick tests
Quick tests can be triggered with the '-q' flag. This sets the house ratio to 100 (default is 2), which means that households will be less well distributed.
However, as a number of calculations are performed on the house level (not the household level), this setting speeds up the code by up to an order of magnitude.
`python3 run.py -q --location=abbottabad --transition_scenario=extend-lockdown --transition_mode=1 --output_dir=output`

Full documentation can be found at: http://facs.readthedocs.io
 
