'''
Luis Contreras-Orendain
CMSC 208 - Final Project


### Test suite

# read in data
'''

import os, os.path

files = []
path = "/home/lcontreras/CMSC208-Final-Project/harry_potter_texts/"

for filename in os.listdir(path):
    print(filename)
    files.append(open(path + filename, "r").decode("utf8").read().split())

print(files[0][0])
