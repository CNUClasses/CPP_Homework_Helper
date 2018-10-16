#get a list of files
from glob import glob
import os
import subprocess_tut

# the parent directory where I'm running the eclipse C++ project
eclipse_clean_dir = "/home/keith/eclipse-workspace/327_proj3_test/"
eclipse_test_dir = "/home/keith/eclipse-workspace/327_proj3_test/src/"
eclipse_fileio_dir = "/home/keith/eclipse-workspace/327_proj3_fileIO/"
eclipse_stringparser_dir = "/home/keith/eclipse-workspace/327_proj3_stringparser/"

test_file = "327_proj3_test.cpp"
fileio_file = "FileIO.cpp"
stringparser_file = "StringParserClass.cpp"

test_FQN            =eclipse_test_dir + test_file
fileio_FQN          =eclipse_fileio_dir + fileio_file
stringparser_FQN    =eclipse_stringparser_dir + stringparser_file

where_student_files_are_dir = "/home/keith/Desktop/327_proj_testing/proj3_2/"
script_output_results = "stdout.txt"

filelist = glob(where_student_files_are_dir + "*.cpp")
filelist.sort()

#redirect output
out = open(script_output_results,"w")
for file in filelist:
    #bb format is   Project1_00767120_attempt_2017-09-15-19-05-17_utilities
    #2nd group is student id
    delims = file.split("_")
    student_id = "----------------------FOR_STUDENT_" + delims[4] + "--------------------------------"
    # student_id = "----------------------FOR_STUDENT_" + delims[3]+"--------------------------------"
    print(student_id)

    if (test_file in file):
        #remove old
        cmds = "echo " + student_id + ";rm " + test_FQN
        process = subprocess_tut.Popen(cmds, shell=True, stdout=out, stderr=out)
        process.wait()

        # copy in student files
        cmds = "cp \"" + file + "\"  \"" + test_FQN + "\""
        process = subprocess_tut.Popen(cmds, shell=True, stdout=out, stderr=out)
        process.wait()

    if (fileio_file in file):
        # remove old
        cmds = "echo " + student_id + ";rm " + fileio_FQN
        process = subprocess_tut.Popen(cmds, shell=True, stdout=out, stderr=out)
        process.wait()

        # copy in student files
        cmds = "cp \"" + file + "\"  \"" + fileio_FQN+ "\""
        process = subprocess_tut.Popen(cmds, shell=True, stdout=out, stderr=out)
        process.wait()

    if (stringparser_file in file):
        # remove old
        cmds = "echo " + student_id + ";rm " + stringparser_FQN
        process = subprocess_tut.Popen(cmds, shell=True, stdout=out, stderr=out)
        process.wait()

        # copy in student files
        cmds = "cp \"" + file + "\"  \"" + stringparser_FQN+ "\""
        process = subprocess_tut.Popen(cmds, shell=True, stdout=out, stderr=out)
        process.wait()

        #you can comment out the following lines, set a breakpoint on above process.wait
        # then step through this program to breakpoint
        # and then debug student code in eclipse
        # cmds = "cd " + eclipse_clean_dir + ";cd ./Debug;make clean;make all;"
        # process = subprocess.Popen(cmds, shell=True, stdout=out,stderr=out)
        # process.wait()

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

