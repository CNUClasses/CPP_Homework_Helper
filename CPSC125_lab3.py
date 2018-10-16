#get a list of files
from glob import glob
import os
import subprocess

# the parent directory where I'm running the eclipse C++ project
dir_prog = "/home/keith/PycharmProjects/125_lab3/"


# dir_joblist = "/home/keith/eclipse-workspace/Proj2_410_queues_SOLUTION/joblist/"
# eclipse_project_dir = "/home/keith/eclipse-workspace/Proj2_410_queues_SOLUTION/"
# eclipse_exec = "/home/keith/eclipse-workspace/Proj2_410_queues_SOLUTION/Debug/Proj2_410_queues_SOLUTION"
where_student_files_are_dir = "/home/keith/Desktop/125_projects/lab3/"
script_output_results = "125_Lab3.txt"

filelist = glob(where_student_files_are_dir + "*.py")
# filelist.sort()
def getFile(id, name = "joblist"):
    for file in filelist:
        if id in file:
            if name in file:
                print(file)
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
    printnbrs = getFile(id, "printnbrs")
    # file_utilities = getFile(id,"utilities")
    if printnbrs == None:
        print("Student " + id + " failed to include printnbrs.py")

    lettertonbr = getFile(id, "lettertonbr")
    # file_utilities = getFile(id,"utilities")
    if lettertonbr == None:
        print("Student " + id + " failed to include lettertonbr.py")

    #remove dispatcher.cpp and joblist.cpp
    cmds1 = "echo " + student_id + ";rm " + dir_prog + "printnbrs.py"
    cmds2 = "echo " + student_id + ";rm " + dir_prog + "lettertonbr.py"

    process = subprocess.Popen(cmds1, shell=True, stdout=out, stderr=out)
    process.wait()
    process = subprocess.Popen(cmds2, shell=True, stdout=out, stderr=out)
    process.wait()

    #copy in 2 files (dispatcher and joblist)
    if printnbrs != None:
        cmds = "cp \"" + printnbrs + "\"  \"" + dir_prog + "printnbrs.py\""
        process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
        process.wait()

    if lettertonbr != None:
        cmds = "cp \"" + lettertonbr + "\"  \"" + dir_prog + "lettertonbr.py\""
        process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
        process.wait()


    #now delete the tested files
    if printnbrs != None:
        cmds1 = 'echo ' + student_id + ';rm "' + printnbrs+'"'
        process = subprocess.Popen(cmds1, shell=True, stdout=out, stderr=out)
        process.wait()

    if lettertonbr != None:
        cmds2 = 'echo ' + student_id + ';rm "' + lettertonbr+'"'
        process = subprocess.Popen(cmds2, shell=True, stdout=out, stderr=out)
        process.wait()

    # #you can comment out the following lines, set a breakpoint on above process.wait
    # # then step through this program to breakpoint
    # # and then debug student code in eclipse
    #
    # #clean
    # cmds = "cd " + dir_prog + ";cd ./Debug;make clean;"
    # process = subprocess.Popen(cmds, shell=True, stdout=out,stderr=out)
    # process.wait()
    #
    # # build
    # cmds = "cd " + dir_prog + ";cd ./Debug;make;"
    # process = subprocess.Popen(cmds, shell=True, stdout=out,stderr=out)
    # process.wait()
    #
    #
    # #run the exe
    # cmds = "cd " + dir_prog + ";./Debug/Proj1_410_solution"
    # process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    # process.wait()

    i=3

    # try:
    #     # wanna see its output with 2 few params?
    #     # subprocess.check_output([self.cmd_file, self.data_file, passfile])
    #     print(subprocess.check_output([eclipse_exec]))
    # except subprocess.CalledProcessError as err:
    #     print("Problems...", "Utility returned:" + str(err.returncode) + " " + err.output)
    # else:
    #     print("No worries", "SUCCESS")


out.close

