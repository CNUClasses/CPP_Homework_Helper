#get a list of files
from glob import glob
import os
import subprocess_tut
import subprocess

# the parent directory where I'm running the eclipse C++ project
dir_cpp_files = "/home/keith/eclipse-workspace_MESSED_UP/410_project3_solution/src/"

eclipse_project_dir = "/home/keith/eclipse-workspace_MESSED_UP/410_project3_solution/"
eclipse_exec = "/home/keith/eclipse-workspace_MESSED_UP/410_project3_solution/Debug/410_project3_solution"
where_student_files_are_dir = "/home/keith/Desktop/student_projects/410/proj3/f19/"


script_output_results = "410_proj3.txt"

tmpdir = os.path.join(where_student_files_are_dir,"*.*")
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
     studentids.add(delims[2])

studentids = sorted(studentids)


for id in studentids:

    student_id = "----------------------FOR_STUDENT_" + id +"--------------------------------"
    print(student_id)

    # get the 2 files to copy
    file_tester = getFile(id, "tester")
    file_print_ts = getFile(id, "print_ts")
    file_answers = getFile(id, "answers")

    if(file_answers==None):
        file_answers = ""
    elif (file_tester == None):
        print("No tester.cpp")
        continue
    elif (file_print_ts == None):
        print("No print_ts.cpp")
        continue

    #remove tester.cpp and print_ts.cpp
    cmds1 = "echo " + student_id + ";rm " + dir_cpp_files + "tester.cpp"
    cmds2 = "echo " + student_id + ";rm " + dir_cpp_files + "print_ts.cpp"
    cmds3 = "echo " + student_id + ";rm " + dir_cpp_files + "answers.txt"

    process = subprocess.Popen(cmds1, shell=True, stdout=out, stderr=out)
    process.wait()
    process = subprocess.Popen(cmds2, shell=True, stdout=out, stderr=out)
    process.wait()
    process = subprocess.Popen(cmds3, shell=True, stdout=out, stderr=out)
    process.wait()

    # clear out .txt files
    # cmds1 = "cd " + eclipse_project_dir + ";rm *.txt"
    # process = subprocess_tut.Popen(cmds1, shell=True, stdout=out, stderr=out)
    # process.wait()

    #copy in 2 files (tester and print_ts)
    cmds = "cp \"" + file_tester + "\"  \"" + dir_cpp_files + "tester.cpp\""
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

    cmds = "cp \"" + file_print_ts + "\"  \"" + dir_cpp_files + "print_ts.cpp\""
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

    cmds = "cp \"" + file_answers + "\"  \"" + dir_cpp_files + "answers.txt\""
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

    pass

    #run the process and capture its output
    cmds = "cd "+ eclipse_project_dir+ ";./Debug/410_proj4_solution "
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    stdout,stderr = process.communicate(student_id)
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

