#get a list of files
from glob import glob
import os
import subprocess

# the parent directory where I'm running the eclipse C++ project
dir_dispatcher = "/home/keith/eclipse-workspace_MESSED_UP/Proj2_410_queues_SOLUTION/dispatcher/"
dir_joblist = "/home/keith/eclipse-workspace_MESSED_UP/Proj2_410_queues_SOLUTION/joblist/"
eclipse_project_dir = "/home/keith/eclipse-workspace_MESSED_UP/Proj2_410_queues_SOLUTION/"
eclipse_exec = "/home/keith/eclipse-workspace_MESSED_UP/Proj2_410_queues_SOLUTION/Debug/Proj2_410_queues_SOLUTION"
where_student_files_are_dir = "/home/keith/Desktop/410/proj2/s19/q/"


script_output_results = "410_proj2.txt"

tmpdir = os.path.join(where_student_files_are_dir,"*.cpp")
filelist = glob(tmpdir )
# filelist.sort()
def getFile(id, name = "joblist"):
    for file in filelist:
        if id in file:
            if name in file:
                return file


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

    # get the 2 files to copy
    file_joblist = getFile(id,"joblist")
    file_dispatcher = getFile(id, "dispatcher")

    #remove dispatcher.cpp and joblist.cpp
    cmds1 = "echo " + student_id + ";rm " + dir_dispatcher + "dispatcher.cpp"
    cmds2 = "echo " + student_id + ";rm " + dir_joblist + "joblist.cpp"

    process = subprocess.Popen(cmds1, shell=True, stdout=out, stderr=out)
    process.wait()
    process = subprocess.Popen(cmds2, shell=True, stdout=out, stderr=out)
    process.wait()

    # clear out .txt files
    cmds1 = "cd " + eclipse_project_dir + ";rm *.txt"
    process = subprocess.Popen(cmds1, shell=True, stdout=out, stderr=out)
    process.wait()

    #copy in 2 files (dispatcher and joblist)
    cmds = "cp \"" + file_joblist +"\"  \"" + dir_joblist + "joblist.cpp\""
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

    cmds = "cp \"" + file_dispatcher + "\"  \"" + dir_dispatcher + "dispatcher.cpp\""
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

    #you can comment out the following lines, set a breakpoint on above process.wait
    # then step through this program to breakpoint
    # and then debug student code in eclipse

    #run the build in eclipse
    pass
    cmds = "cd " + eclipse_project_dir + ";cd ./Debug;make clean;make;"
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

    # run the exe
    cmds = "cd " + eclipse_project_dir + ";./Debug/Proj2_410_queues_SOLUTION"
    process = subprocess.Popen(cmds, shell=True, stdout=out,stderr=out)
    process.wait()


    # run plot_proceses.py to show resyults
    pass
    # cmds = "cd " + eclipse_project_dir + ";cd ./plotProcesses;python plot_processes.py"
    # process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    # process.wait()


    # try:
    #     # wanna see its output with 2 few params?
    #     # subprocess.check_output([self.cmd_file, self.data_file, passfile])
    #     print(subprocess.check_output([eclipse_exec]))
    # except subprocess.CalledProcessError as err:
    #     print("Problems...", "Utility returned:" + str(err.returncode) + " " + err.output)
    # else:
    #     print("No worries", "SUCCESS")


out.close

