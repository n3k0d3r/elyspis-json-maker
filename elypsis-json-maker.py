#!/usr/bin/python

import sys
import os.path
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

# Color variants
colors = {
    "white",
    "orange",
    "magenta",
    "light_blue",
    "yellow",
    "lime",
    "pink",
    "gray",
    "light_gray",
    "cyan",
    "blue",
    "purple",
    "green",
    "brown",
    "red",
    "black"
}

# Open and read in file given
print("Opening file '%s'" % filename)
f = open(filename, "r")
config = f.read().split(";")
f.close()

# Strip whitespace, pull colored variants and add to list in each color
config = [each.strip() for each in config]
variants = [each for each in config if re.search("@color", each)]
config = [each for each in config if each not in variants]
for each in variants:
    for color in colors:
        config.append(each.replace("@color", color))


print(config)
print(variants)