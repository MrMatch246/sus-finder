# sus-finder
Find suspiciouns strings in services

Usage: python3 sus_finder.py [path/to/config.json] 

Output will be located in per service seperated txt files
in the specified output folder if existent or otherwise in repo/results

sus.txt supports extended grep patterns, severity, and applicable file types

TODO:  add the checking for filetype to pattern_list_gen
and use it 
(unsure if this is actually usefull considering files having code from other types in them like inline asm in c or bash in python) 
