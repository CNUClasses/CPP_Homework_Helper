
from glob import glob
import os
import subprocess

functions = "Functions.cpp"
smalltalk = "Smalltalk.cpp"
target_dir = '/home/keith/Desktop/327_projects/327proj4/all/'
target_dir_func = '/home/keith/Desktop/327_projects/327proj4/all/functions/'
target_dir_st = '/home/keith/Desktop/327_projects/327proj4/all/smalltalk/'

#create functions dir
import os
if not os.path.exists(target_dir_func):
    os.makedirs(target_dir_func)

if not os.path.exists(target_dir_st):
    os.makedirs(target_dir_st)

# get a list of student files
filelist = glob(target_dir + "*.cpp")
filelist.sort()

for f in filelist:
    if functions in f:
        fn1 = os.path.basename(f)
        cmds = "cp \"" + f + "\"  \"" + target_dir_func +fn1+ "\""
        process = subprocess.Popen(cmds, shell=True)
        process.wait()
    elif smalltalk in f:
        fn1 = os.path.basename(f)
        cmds = "cp \"" + f + "\"  \"" + target_dir_st + fn1 + "\""
        process = subprocess.Popen(cmds, shell=True)
        process.wait()




