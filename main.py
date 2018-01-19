#!/usr/bin/env python

"""img2model.py: Takes a bitmap image and converts it, via several steps, into a model"""

__author__ = "David Clarke"
__copyright__ = "Copyright 2018"
__credits__ = ["David Clarke", "Blender Foundation", "Peter Selinger"]
__license__ = "GPL"
__version__ = "3"
__maintainer__ = "David Clarke"
__email__ = "dac531@york.ac.uk"
__status__ = "In Development"

import os
import subprocess

import _blenderscript

# verify potrace included

if not os.path.isfile("potrace.exe"):
    raise RuntimeError("Missing dependancy: 'potrace.exe' could not be found")

# verify folder structure exists
for path in ["bmp","svg","out"]:
    if not os.path.exists(path):
        os.mkdir(path)

# define job params from files

files = os.listdir("bmp\\")
models = {}
if len(files) == 0:
    raise ValueError("No Input: No bitmap files detected")
for file in files:
    if not file.endswith(".bmp"):
        raise RuntimeError("File Error: All input files in '/bmp/' must be of type bitmap, with extension '.bmp'")
    data = file.split("-")
    key = data[0]
    try:
        extrusion = float(data[len(data)-1][:len(data[len(data)-1])-4:])
    except:
        raise RuntimeError("File Error: One or more files in '/bmp/' is in the incorrect format '<group>-<extrusion>.bmp")

    noext_file = file[:len(file)-4:]
    
    if key in models:
        models[key].append((extrusion,noext_file))
    else:
        models[key] = [(extrusion,noext_file)]

# create svg files from bitmap using potrace

subprocess.run("potrace.exe -s bmp\*.bmp",check=True)
for file in os.listdir("bmp\\"):
    if file.endswith(".svg"):
        fpi = os.path.join("bmp", file)
        fpo = os.path.join("svg", file)
        try:
            os.rename(fpi, fpo)
        except:
            os.remove(fpi)            

# locate blender installation from path

paths = os.environ.get("PATH").split(";")
blend_path = False
for path in paths:
    fp = os.path.join(path, "blender.exe")
    if os.path.isfile(fp):
        blend_path = fp
        break
if not blend_path:
    raise RuntimeError("Path Error: Could not find blender in path. Please add it to the path variable")
print("Found blender executable: '" + blend_path + "'")

# import each layer into blender and export as a temp model

blendcode = _blenderscript.code
for group in models:
    for model in models[group]:
        fpi = os.path.abspath(os.path.join("svg",(model[1] + ".svg")))
        ext = model[0]
        fpo = os.path.abspath((os.path.join("out",(model[1] + ".3ds"))))

        modelcode = blendcode.format(fpi,ext,repr(fpo).replace("'", ""))
        with open("_blendjob.py", "w") as f:
            f.write(modelcode)
            print("Attempted write")
        processcmd = blend_path + " -b -P _blendjob.py"
        subprocess.run(processcmd, check=True)
        #os.remove("_blendjob.py")
print("END")
