#get a list of files
from glob import glob
import os
import subprocess

'''
NOTE: Change test.cpp 
TEST_STRING, TEST_STRING_NO_END_TAG, TEST_STRING_NO_START_TAG  to have <to1> and </to1> tags!!!!!!!!!

'''


# the parent directory where I'm running the eclipse C++ project
# dir_cpp_files = "/home/keith/eclipse-workspace/Proj3_Library_Vector_SOLUTION/library/"
eclipse_workspace_dir = "/home/keith/git/"

eclipse_FileIO = eclipse_workspace_dir + "327_proj3_fileIO/"
eclipse_stringparser = eclipse_workspace_dir + "327_proj3_stringparser/"
eclipse_327_proj3_test = eclipse_workspace_dir + "327_proj3_test/src/"
eclipse_project_dir = eclipse_workspace_dir + "327_proj3_test/"
output_file = eclipse_workspace_dir + "327_proj3_test/output/"

# here are the command arguments
cmd_line_params = " './data/testdata_full.txt' '<to1>' '</to1>' './output/outfile1.txt'"

# CHANGE THESE FILES
# where_student_files_are_dir = "/home/keith/Desktop/327_projects/327_proj4_stringParser/s19/"s19p270s
where_student_files_are_dir = "/home/keith/Desktop/student_projects/327_projects/327_proj4_stringParser/f19/late/"

# where_student_files_are_dir =   "/home/keith/Desktop/327_projects/327proj4/s18problems/"
script_output_results = "./stdoutCf19-Proj4.txt"

# script_output_results = "./stdoutCf18-Proj4.txt"
DELIM_WITH_STUDENTID=5
# DELIM_WITH_STUDENTID=1
tmpdir = os.path.join(where_student_files_are_dir,"*.cpp")
filelist = glob(tmpdir )
filelist.sort()

def getFile(id, name ):
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
     studentids.add(delims[DELIM_WITH_STUDENTID])
studentids = sorted(studentids)

# remove stdout.txt here
# cmds1 = "rm ./" + script_output_results
# process = subprocess.Popen(cmds1, shell=True, stdout=out, stderr=out)
# process.wait()

def clean_and_build(project_dir):
    global cmds, process
    cmds = "cd " + project_dir + ";cd ./Debug;make clean;make;"
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()


for id in studentids:

    student_id = "----------------------FOR_STUDENT_" + id +"--------------------------------"
    print(student_id)

    # get the 2 files to copy
    file_fileIO = getFile(id, "FileIO")
    file_StringParser = getFile(id, "StringParser")
    file_327_proj3_test = getFile(id, "test")

    #remove above
    cmds1 = "echo " + student_id + ";rm " + eclipse_FileIO + "FileIO.cpp"
    cmds2 = "echo " + student_id + ";rm " + eclipse_stringparser + "StringParserClass.cpp"
    cmds3 = "echo " + student_id + ";rm " + eclipse_327_proj3_test + "327_proj3_test_student"
    process = subprocess.Popen(cmds1, shell=True, stdout=out, stderr=out);process.wait()
    process = subprocess.Popen(cmds2, shell=True, stdout=out, stderr=out);process.wait()
    process = subprocess.Popen(cmds3, shell=True, stdout=out, stderr=out);process.wait()

    # clear out .txt files
    cmds1 = "cd " + output_file + ";rm *.txt"
    process = subprocess.Popen(cmds1, shell=True, stdout=out, stderr=out);process.wait()




    #copy in 3 files
    cmds = "cp \"" + file_fileIO + "\"  \"" + eclipse_FileIO + "FileIO.cpp\""
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

    cmds = "cp \"" + file_StringParser + "\"  \"" + eclipse_stringparser + "StringParserClass.cpp\""
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

    # for this one copy and check that it verifies 5 arguments and then extracts them from commandline
    if file_327_proj3_test!=None:
        cmds = "cp \"" + file_327_proj3_test + "\"  \"" + eclipse_327_proj3_test + "327_proj3_test_student\""
        process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
        process.wait()

    #build the libraries first then the tester
    clean_and_build(eclipse_FileIO)
    clean_and_build(eclipse_stringparser)
    clean_and_build(eclipse_project_dir)

    #run the process and capture its output
    cmds = "cd "+ eclipse_project_dir+ ";./Debug/327_proj3_test " + cmd_line_params
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    stdout,stderr = process.communicate(student_id)
    process.wait()


    i=1

out.close

