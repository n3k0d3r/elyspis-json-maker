#!/usr/bin/python

import sys
import os.path
import shutil
import re
import fileinput

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

# Get template data
f = open("stonecutter-template.json", "r")
stonecutter_template = f.read()
f.close()
f = open("shapeless-template.json", "r")
shapeless_template = f.read()
f.close()
f = open("shapeless-slab-template.json", "r")
shapeless_slab_template = f.read()
f.close()
f = open("shaped-template.json", "r")
shaped_template = f.read()
f.close()

# Output directory
output_dir = "output"
if(os.path.exists(output_dir)):
    shutil.rmtree(output_dir)
try:
    os.makedirs(output_dir)
except PermissionError:
    print("Windows 10 permissions are dumb. Run the script again lol")
    exit()

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

'''
    Break out stonecutter, shapeless, and shaped into their colored variants, write to file
    I noticed I could consolidate these into a single loop, but it is late and I am lazy.
    Maybe another day.
'''
for block_in in stonecutting_in:
    blocks_out = stonecutting_in[block_in]
    if(block_in[0] == "&"):
        for color in colors:
            final_block_in = block_in[1:].replace("@color", color)
            if(":" not in final_block_in):
                final_block_in = "elypsis:%s" % final_block_in
            for each in blocks_out:
                if(":" not in each):
                    each = "elypsis:%s" % each.replace("@color", color)
                output = (final_block_in+"_to_"+each).replace(":", "_").encode("utf-8", "ignore").decode().lower()
                f = open("output/stonecutter_%s.json" % output, "w")
                f.write(stonecutter_template.replace("$item", final_block_in)
                                            .replace("$result", each)
                                            .replace("$count", "2" 
                                                if any(double in each for double in ["slab", "stairs", "pillar"]) 
                                                else "1"))
                f.close()
    else:
        if(":" not in block_in):
            block_in = "elypsis:%s" % block_in
        for each in blocks_out:
            if(":" not in each):
                each = "elypsis:%s" % each
            output = (block_in+"_to_"+each).replace(":", "_").encode("utf-8", "ignore").decode().lower()
            f = open("output/stonecutter_%s.json" % output, "w")
            f.write(stonecutter_template.replace("$item", block_in)
                                        .replace("$result", each)
                                        .replace("$count", "2"
                                            if any(double in each for double in ["slab", "stairs", "pillar"])
                                            else "1"))
            f.close()

for block_in in shapeless_in:
    blocks_out = shapeless_in[block_in]
    if(block_in[0] == "&"):
        for color in colors:
            final_block_in = block_in[1:].replace("@color", color)
            if(":" not in final_block_in):
                final_block_in = "elypsis:%s" % final_block_in
            for each in blocks_out:
                if(":" not in each):
                    each = "elypsis:%s" % each.replace("@color", color)
                output = (final_block_in+"_to_"+each).replace(":", "_").encode("utf-8", "ignore").decode().lower()
                f = open("output/shapeless_%s.json" % output, "w")
                template = shapeless_slab_template if any(double in final_block_in for double in ["slab", "stairs", "pillar"]) else shapeless_template
                f.write(template.replace("$item", final_block_in)
                                .replace("$result", each)
                                .replace("$count", "2" 
                                    if any(double in each for double in ["slab", "stairs", "pillar"]) 
                                    else "1"))
                f.close()
    else:
        if(":" not in block_in):
            block_in = "elypsis:%s" % block_in
        for each in blocks_out:
            if(":" not in each):
                each = "elypsis:%s" % each
            output = (block_in+"_to_"+each).replace(":", "_").encode("utf-8", "ignore").decode().lower()
            f = open("output/shapeless_%s.json" % output, "w")
            template = shapeless_slab_template if any(double in block_in for double in ["slab", "stairs", "pillar"]) else shapeless_template
            f.write(template.replace("$item", block_in)
                            .replace("$result", each)
                            .replace("$count", "2"
                                if any(double in each for double in ["slab", "stairs", "pillar"])
                                else "1"))
            f.close()

'''for block_in in shaped_in:
    blocks_out = shaped_in[block_in]
    if(block_in[0] == "&"):
        for color in colors:
            final_block_in = block_in[1:].replace("@color", color)
            if(":" not in final_block_in):
                final_block_in = "elypsis:%s" % final_block_in
            for each in blocks_out:
                if(":" not in each):
                    each = "elypsis:%s" % each.replace("@color", color)
                output = (final_block_in+"_to_"+each).replace(":", "_").encode("utf-8", "ignore").decode().lower()
                f = open("output/shaped_%s.json" % output, "w")
                f.write(shaped_template.replace("$item", final_block_in)
                                       .replace("$result", each)
                                       .replace("$count", "2"
                                            if any(double in each for double in ["slab", "stairs", "pillar"]) 
                                            else "1"))
                f.close()
    else:
        if(":" not in block_in):
            block_in = "elypsis:%s" % block_in
        for each in blocks_out:
            if(":" not in each):
                each = "elypsis:%s" % each
            output = (block_in+"_to_"+each).replace(":", "_").encode("utf-8", "ignore").decode().lower()
            f = open("output/shaped_%s.json" % output, "w")
            f.write(shaped_template.replace("$item", block_in)
                                   .replace("$result", each)
                                   .replace("$count", "2"
                                        if any(double in each for double in ["slab", "stairs", "pillar"])
                                        else "1"))
            f.close()
'''