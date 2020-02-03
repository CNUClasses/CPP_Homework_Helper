# get a list of files
from glob import glob
import os
import subprocess
import zipfile, os
import sys
import logging

# where the student files are
where_student_files_are_dir = "/home/keith/Desktop/student_projects/410/proj4/f19/"
# the parent directory where I'm running the eclipse C++ project
eclipse_clean_dir = "/home/keith/eclipse-workspace_MESSED_UP/410_proj4_Solution/"

# //where to copy all the student files
baker_dir = "/home/keith/eclipse-workspace_MESSED_UP/410_proj4_Solution/baker/"
waiter_dir = "/home/keith/eclipse-workspace_MESSED_UP/410_proj4_Solution/waiter/"
logger_dir = "/home/keith/eclipse-workspace_MESSED_UP/410_proj4_Solution/logger/"
script_output_results = "410_p4stdout_s19s1.txt"

# make and clean here
proj = "/home/keith/eclipse-workspace_MESSED_UP/410_proj4_Solution/"

# expected files in submission
baker = "Baker.cpp"  # will not copy to a cpp file so not compileable
waiter = "waiter.cpp"
logger = "logger.cpp"

DELIM_WITH_STUDENTID = 2

# redirect output
out = open(script_output_results, "w")

# get a list of student files
filelist = glob(where_student_files_are_dir + "*.cpp")
filelist.sort()

def getFile(id, name ):
    for file in filelist:
        if id in file:
            if name in file:
                return file

# get a list of unique student ids
studentids=set()
for file in filelist:
     delims = file.split("_")
     studentids.add(delims[DELIM_WITH_STUDENTID])
studentids = sorted(studentids)

def clean_and_build(project_dir):
    global cmds, process
    cmds = "cd " + project_dir + ";cd ./Debug;make clean;"
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()
    cmds = "cd " + project_dir + ";cd ./Debug;make;"
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

for id in studentids:
    student_id = "----------------------FOR_STUDENT_" + id +"--------------------------------"
    print(student_id)

    # get files to copy
    file_logger = getFile(id, "logger")
    file_baker = getFile(id, "Baker")
    file_waiter = getFile(id, "waiter")

    #remove files that are already there
    cmds1 = "echo " + student_id + ";rm " + baker_dir + baker
    cmds2 = "echo " + student_id + ";rm " + waiter_dir + waiter
    cmds3 = "echo " + student_id + ";rm " + logger_dir + logger
    process = subprocess.Popen(cmds1, shell=True, stdout=out, stderr=out);
    process.wait()
    process = subprocess.Popen(cmds2, shell=True, stdout=out, stderr=out);
    process.wait()
    process = subprocess.Popen(cmds3, shell=True, stdout=out, stderr=out);
    process.wait()

    # remove output files

     # copy in  files
    cmds = "cp \"" + file_logger + "\"" + " \"" + logger_dir + logger+ "\""
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()
    cmds = "cp \"" + file_waiter + "\"" + " \"" + waiter_dir + waiter + "\""
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()
    cmds = "cp \"" + file_baker + "\"" + " \"" + baker_dir + baker + "\""
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

    # make_and_clean()
    clean_and_build(proj)

    #run the process and capture its output
    # cmds = "cd "+ proj+ ";pwd;./Debug/410_proj4_Solution "
    # process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    # stdout,stderr = process.communicate(student_id)
    # process.wait()

    pass

out.close
