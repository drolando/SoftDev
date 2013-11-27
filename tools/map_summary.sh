# This scripts prints a summary of the objects in the map
# (the map is stored in xml format under /map/shrine.xml)
# The tool is invoked with the map file as parameter

# By running this tool, the output should be:
# 2449 sands 2
# 2268 water 1
# 361 beach 6
# 306 sign 2
# 267 trees 5
# 193 bushes 5
# 38 rocks 3
# 31 roots 2
# 30 quays 2
# 24 mussels 9
# 23 beebox 1
# 15 empty_lid 1
# 10 bee 1
# 9 starfishes 2
# 3 priest_hut 1
# 2 skull_pole 1
# 2 shrine 1
# 1 hippie_priest 1
# 1 girl 1
# 1 dynamites_lid_broken 1
# 1 chemist 1
# 1 boy 1
# 1 beekeeper 1
# 1 beach_bar 1
#
# Where the first column is the number of elements. The second is the
# object type, and the third is the number of objects subtypes.
# E.g., bushes:05   --> bushes is the name and 05 is the subtype

MAPFILE=$1

# Put here your code

