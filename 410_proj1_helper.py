#get a list of files
from glob import glob
import os
import subprocess

# the parent directory where I'm running the eclipse C++ project
dir_prog = "/home/keith/eclipse-workspace_MESSED_UP/Proj1_410_solution/"


# dir_joblist = "/home/keith/eclipse-workspace/Proj2_410_queues_SOLUTION/joblist/"
# eclipse_project_dir = "/home/keith/eclipse-workspace/Proj2_410_queues_SOLUTION/"
# eclipse_exec = "/home/keith/eclipse-workspace/Proj2_410_queues_SOLUTION/Debug/Proj2_410_queues_SOLUTION"
where_student_files_are_dir = "/home/keith/Desktop/410/proj1/s19/c2messedup/"
script_output_results = "410F_Proj1.txt"

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
     studentids.add(delims[1])
studentids = sorted(studentids)

for id in studentids:

    student_id = "----------------------FOR_STUDENT_" + id +"--------------------------------"
    print(student_id)

    # get the file to copy
    file_utilities = getFile(id,"utilities")
    if file_utilities == None:
        #either isnt there or caps problem
        print("Student " + id + " failed to include utilities.cpp")
        continue



    #remove dispatcher.cpp and joblist.cpp
    cmds1 = "echo " + student_id + ";rm " + dir_prog + "utilities.cpp"
    cmds2 = "echo " + student_id + ";rm " + dir_prog + "results.txt"

    process = subprocess.Popen(cmds1, shell=True, stdout=out, stderr=out)
    process.wait()
    process = subprocess.Popen(cmds2, shell=True, stdout=out, stderr=out)
    process.wait()

    #copy in 2 files (dispatcher and joblist)
    cmds = "cp \"" + file_utilities +"\"  \"" + dir_prog + "utilities.cpp\""
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()


    #you can comment out the following lines, set a breakpoint on above process.wait
    # then step through this program to breakpoint
    # and then debug student code in eclipse

    #clean
    cmds = "cd " + dir_prog + ";cd ./Debug;make clean;"
    process = subprocess.Popen(cmds, shell=True, stdout=out,stderr=out)
    process.wait()

    # build
    cmds = "cd " + dir_prog + ";cd ./Debug;make;"
    process = subprocess.Popen(cmds, shell=True, stdout=out,stderr=out)
    process.wait()


    #run the exe
    cmds = "cd " + dir_prog + ";./Debug/Proj1_410_solution"
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

    pass

    # try:
    #     # wanna see its output with 2 few params?
    #     # subprocess.check_output([self.cmd_file, self.data_file, passfile])
    #     print(subprocess.check_output([eclipse_exec]))
    # except subprocess.CalledProcessError as err:
    #     print("Problems...", "Utility returned:" + str(err.returncode) + " " + err.output)
    # else:
    #     print("No worries", "SUCCESS")


out.close

