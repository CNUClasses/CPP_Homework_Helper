#get a list of files
from glob import glob
import os
import subprocess

# the parent directory where I'm running the eclipse C++ project
eclipse_project_dir = "/home/keith/eclipse-workspace_MESSED_UP/Project2_Solution/src/"
eclipse_exec = "/home/keith/eclipse-workspace_MESSED_UP/Project2_Solution/Debug/Project2_Solution.exe"

where_student_files_are_dir =   "/home/keith/Desktop/327_projects/327proj2/s19/"
# where_student_files_are_dir =   "/home/keith/Desktop/327_projects/327proj2/s18/c1/"

script_output_results = "327_proj2_out.txt"

filelist = glob(where_student_files_are_dir + "*.cpp")
# filelist.sort()

def getFile(id, name = "joblist"):
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
     studentids.add(delims[2])
studentids = sorted(studentids)

for id in studentids:

    student_id = "----------------------FOR_STUDENT_" + id +"--------------------------------"
    print(student_id)

    # get the file to copy
    stud_array_functions = getFile(id, "array_functions")
    if stud_array_functions == None:
        #either isnt there or caps problem
        print("Student " + id + " failed to include array_functions.cpp")
        continue
    # else:
    #     print(stud_array_functions)

    # remove old files copy in new
    cmds1 = "echo " + student_id + ";rm " + eclipse_project_dir + "array_functions.cpp"
    cmds2 = "cp \"" + stud_array_functions +"\"  \"" + eclipse_project_dir + "array_functions.cpp\""

    process = subprocess.Popen(cmds1, shell=True, stdout=out, stderr=out);
    process.wait()
    process = subprocess.Popen(cmds2, shell=True, stdout=out, stderr=out);
    process.wait()

    #clean
    cmds = "cd " + eclipse_project_dir + ";cd ../Debug;make clean;"
    process = subprocess.Popen(cmds, shell=True, stdout=out,stderr=out)
    process.wait()

    # build
    cmds = "cd " + eclipse_project_dir + ";cd ../Debug;make;"
    process = subprocess.Popen(cmds, shell=True, stdout=out,stderr=out)
    process.wait()


    #run the exe
    cmds = "cd " + eclipse_project_dir + ";cd ..;./Debug/Project2_Solution.exe"
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

    pass

out.close

