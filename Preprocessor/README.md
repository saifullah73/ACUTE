# ACUTE Preprocessor


## Obtaining an OSM file.
OSM files are obtained from either Openstreetmaps.org, or using the OSRM tool.  
The OSM files (format osm.pbf) used for this project are already added in this repository.They can be found in OSM directory. In case you want to parse your own custom osm, you can follow the steps below.  
### Data Preparation (optional)
1) Download Pakistan OSM file first, we'll crop out specific cities from it
2) Go to https://www.openstreetmap.org/ and search for a region of choice (eg. Islamabad)
3) In the search results find the boundary object for region labelled as Region boundary
4) Get its id, which is of type 'relation' (combination of nodes and points)
5) To extract polygon (boundary) go to http://polygons.openstreetmap.fr/ and enter id, and download file
6) Save it with name .poly at the same location where Pakistan OSM is saved
7) Now you have your region boundaries and we want to  extract it from Pakistan osm
8) Use the provided tool osmconvert.exe and type the following command `osmconvert <parent osm> -B="<region polygon file>" --complete-ways --complete-multipolygons -o=<output filename>`
9) eg. `osmconvert pakistan.osm -B="islamabad.poly" --complete-ways --complete-multipolygons -o=islamabad.osm.pbf`
10) The osm_parser.py accepts .osm.pbf files. In case you have osm files you can convert them to .pbf format using osmconvert as well.
11) eg `osmconvert i10.osm -o=i10.osm.pbf`
12) You can also download JOSM tool to visualize and edit OSM files

## Installing Requirements
To install requirements run the following command.  
`pip3 install -r requirements.txt` 
Please note that you need to create a conda environment first with python3.8 or above before installing requirements or executing code.  
The soruce code has been executed and tested on ubuntu OS with a conda environment. It may or may not run on Windows systems.  

## Extracting locations
osm_parser.py parses input osm.pbf file, extracts variety of places and outputs a location graph. 
The script accepts multiple parameters as input
1) --input <path to osm.pbf file to parse> : if you skip it the script will use a default osm file  
2) --population: population of a specific region
3) --leisure: to extract leisure places  
4) --schools: to extract schools  
5) --hospitals: to extract hospitals  
6) --offices: to extract offices  
7) --place_of_worship: to extract place of worship  
8) --supermarkets: to extract supermarkets  
9) --houses: to generate houses in residential areas  
10) --merge: to merge individual results of supermarkets, leisure etc  
11) --loc: to use the output of merge to generate location graph  
12) --all: to do all of the above with on the input OSM.  
`python3 osm_parser.py --input ../OSM/islamabad.osm.pbf --population 1129198 --leisure --schools --merge --loc`  
`python3 osm_parser.py --input ../OSM/Abbottabad.osm.pbf --population 200000 --all`  
