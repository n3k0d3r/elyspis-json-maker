#!/usr/bin/python

import sys
import os.path
import shutil
import re

# Check for only 1 argument
if(len(sys.argv) != 2):
    print("Error, requires 1 argument")
    exit()

# Check if given file and templates exist
filename = sys.argv[1].strip()
if(not os.path.exists(filename)):
    print("File '%s' does not exist" % filename)
    exit()
for template in [
    "stonecutter-template.json",
    "shapeless-template.json",
    "shapeless-slab-template.json",
    "shaped-template.json"]:
    if(not os.path.exists(template)):
        print("Template '%s' does not exist" % template)
        exit()

# Output directory
output_dir = "output"
if(os.path.exists(output_dir)):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

# Initialize dicts, state, and delimiter literals
colors = {}
stonecutting_in = {}
shapeless_in = {}
shaped_in = {}
setting = ""
d_char = "~"
sub_d_char = ";"

# Open and read in file given
print("Opening file '%s'" % filename)
f = open(filename, "r")
for line in f:
    # If line has [setting], change state
    if(re.search(r"\[.*\]", line)):
        setting = re.search(r"(?<=\[).*(?=\])", line).group()
    # Line contains config value
    else:
        # Store color dye conversion settings
        if(setting == "colors"):
            color = line[:line.find(d_char)].strip()
            dye = line[line.find(d_char) + 1:].strip()
            colors[color] = dye
        # Store input and output settings loosely in dicts
        else:
            block_in = line[:line.find(d_char)].strip()
            # Prepend input with literal if line contains colors, for easier parsing
            if(re.search(r"@color", line)):
                block_in = "&" + block_in
            line_out = line[line.find(d_char) + 1:].strip()
            blocks_out = [each.strip() for each in line_out.split(sub_d_char)]
            if(setting == "minecraft:stonecutting"):
                stonecutting_in[block_in] = blocks_out
            elif(setting == "minecraft:crafting_shapeless"):
                shapeless_in[block_in] = blocks_out
            elif(setting == "minecraft:crafting_shaped"):
                shaped_in[block_in] = blocks_out
f.close()

# Initialize final dicts
stonecutting = {}
shapeless = {}

'''
    Break out stonecutter and shapeless block colors into their final dicts.
    Shaped dicts is keeping its formatting for dye conversion.
'''
for block_in in stonecutting_in:
    blocks_out = stonecutting_in[block_in]
    if(block_in[0] == "&"):
        for color in colors:
            final_block_in = block_in[1:].replace("@color", color)
            shutil.copyfile(
                "stonecutter-template.json",
                "output/stonecutter-%s.json" % final_block_in.encode("utf-8", "ignore").decode()
            )
            final_blocks_out = [each.replace("@color", each) for each in blocks_out]
            stonecutting[final_block_in] = final_blocks_out
    else:
        stonecutting[block_in] = blocks_out
        
for block_in in shapeless_in:
    blocks_out = shapeless_in[block_in]
    if(block_in[0] == "&"):
        for color in colors:
            final_block_in = block_in[1:].replace("@color", color)
            final_blocks_out = [each.replace("@color", each) for each in blocks_out]
            shapeless[final_block_in] = final_blocks_out
    else:
        shapeless[block_in] = blocks_out
