#get a list of files
from glob import glob
import os
import subprocess

# the parent directory where I'm running the eclipse C++ project
dir_cpp_files = "/home/keith/eclipse-workspace_MESSED_UP/Proj3_Library_Vector_SOLUTION/library/"
eclipse_project_dir = "/home/keith/eclipse-workspace_MESSED_UP/Proj3_Library_Vector_SOLUTION/"
output_file = "/home/keith/eclipse-workspace_MESSED_UP/Proj3_Library_Vector_SOLUTION/"


# CHANGE THESE FILES
where_student_files_are_dir = "/home/keith/Desktop/327_projects/327proj3/s19/"
script_output_results = "out_327_proj3_2.txt"
DELIM_WITH_STUDENTID=2

tmpdir = os.path.join(where_student_files_are_dir,"*.cpp")
filelist = glob(tmpdir )
filelist.sort()
def getFile(id, name ):
    for file in filelist:
        if id in file:
            if name in file:
                return file
    return None

#redirect output
out = open(script_output_results,"w")

# get a list of unique student ids
studentids=set()
for file in filelist:
     delims = file.split("_")
     studentids.add(delims[DELIM_WITH_STUDENTID])

studentids = sorted(studentids)

# remove stdout.txt here
cmds1 = "rm stdout.txt"
process = subprocess.Popen(cmds1, shell=True, stdout=out, stderr=out)
process.wait()

for id in studentids:

    student_id = "----------------------FOR_STUDENT_" + id +"--------------------------------"
    print(student_id)

    # get the 2 files to copy
    file_fileIO = getFile(id, "fileIO")
    file_library = getFile(id, "library")

    if (file_fileIO ==None):
        print("MISSING fileIO.cpp")
        continue

    if (file_library == None):
        print("MISSING library.cpp")
        continue

    #remove fileIO.cpp and library.cpp
    cmds1 = "echo " + student_id + ";rm " + dir_cpp_files + "fileIO.cpp"
    cmds2 = "echo " + student_id + ";rm " + dir_cpp_files + "library.cpp"
    process = subprocess.Popen(cmds1, shell=True, stdout=out, stderr=out)
    process.wait()
    process = subprocess.Popen(cmds2, shell=True, stdout=out, stderr=out)
    process.wait()

    # clear out .txt files
    cmds1 = "cd " + eclipse_project_dir + ";rm *.txt"
    process = subprocess.Popen(cmds1, shell=True, stdout=out, stderr=out)
    process.wait()


    #copy in 2 files (dispatcher and library)
    cmds = "cp \"" + file_fileIO + "\"  \"" + dir_cpp_files + "fileIO.cpp\""
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

    cmds = "cp \"" + file_library + "\"  \"" + dir_cpp_files + "library.cpp\""
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

    #run the build in eclipse
    cmds = "cd " + eclipse_project_dir + ";cd ./Debug;make clean;make;"
    # cmds = "cd " + eclipse_project_dir + ";make clean;make;"

    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

    #run the process and capture its output
    cmds = "cd ~/eclipse-workspace_MESSED_UP/Proj3_Library_Vector_SOLUTION;./Debug/Proj3_Library_Vector_SOLUTION "

    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    stdout,stderr = process.communicate(student_id)
    process.wait()


out.close

