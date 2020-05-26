#!/usr/bin/python

import sys
import os.path
import shutil
import re

# Check for only 1 argument
if(len(sys.argv) != 2):
    print("Error, requires 1 argument")
    exit()

# Check if file exists
filename = sys.argv[1].strip()
if(not os.path.exists(filename)):
    print("File '%s' does not exist" % filename)
    exit()

# Output directory
output_dir = "output"
if(os.path.exists(output_dir)):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

# Open and read in file given
colors = {}
stonecutting = {}
shapeless = {}
shaped = {}
setting = ""
d_char = ":"
sub_d_char = ";"
print("Opening file '%s'" % filename)
f = open(filename, "r")
for line in f:
    if(re.search(r"\[.*\]", line)):
        setting = re.search(r"(?<=\[).*(?=\])", line).group()
    else:
        if(setting == "colors"):
            color = line[:line.find(d_char)].strip()
            dye = line[line.find(d_char) + 1:].strip()
            colors[color] = dye
f.close()
print(colors)

# Strip whitespace, pull colored variants and add to list in each color
'''config = [each.strip() for each in config]
variants = [each for each in config if re.search("@color", each)]
config = [each for each in config if each not in variants]
for each in variants:
    for color in colors:
        config.append(each.replace("@color", color))


print(config)
print(variants)'''