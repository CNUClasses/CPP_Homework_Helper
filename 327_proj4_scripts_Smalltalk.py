#get a list of files
from glob import glob
import os
import subprocess
import sys

# CHANGE THESE
where_student_files_are_dir = "/home/keith/Desktop/327_projects/327proj5_smalltalk/s19nocompile/"
DELIM_WITH_STUDENTID=3
efis = 5  #expected number of files to see
script_output_results = "327_project4_scripts_smalltalk_s19.txt"

# where to copy all the student files
eclipse_lib_dir= "/home/keith/git/327_Proj5_Lib/"
eclipse_proj_dir= "/home/keith/git/327_Proj5/"

def clean_and_build():
    # clean
    cmds = "cd " + eclipse_lib_dir + ";cd ./Debug;make clean;"
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()
    cmds = "cd " + eclipse_proj_dir + ";cd ./Debug;make clean;"
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

    # build
    cmds = "cd " + eclipse_lib_dir + ";cd ./Debug;make;"
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()
    cmds = "cd " + eclipse_proj_dir + ";cd ./Debug;make;"
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()


# expected files in submission
proj4 = "327_Proj5" #will not copy to a cpp file so not compileable
functions = "Functions.cpp"
sta= "Smalltalk_American.cpp"
stb = "Smalltalk_Brit.cpp"
st = "Smalltalk.cpp"
stade = "ST_American_DonutEnthusiest.cpp"

   # 6 for most
numb_efis_seen = 0
student_id = ''

def remove_file(fn):
    # remove old
    ftr = eclipse_lib_dir + fn
    cmds = "echo " + student_id + ";rm " + ftr
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

def movefiles(stud_file, fn):
    global numb_efis_seen

    remove_file(fn)

    ftr = eclipse_lib_dir + fn
    # copy in student files
    cmds = "cp \"" + stud_file + "\"  \"" + ftr + "\""
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

    print("     copied " + fn)

    # want to copy efis files and then pause to run diagnostics
    numb_efis_seen += 1

# get a list of student files
filelist = glob(where_student_files_are_dir + "*.cpp")
filelist.sort()

#redirect output
out = open(script_output_results,"w")
for file in filelist:
    # numb_efis_seen

    delims = file.split("_")
    if(student_id != delims[DELIM_WITH_STUDENTID]):
        if (numb_efis_seen !=efis  and len(student_id) !=0):
            print("   WARNING" + student_id + "not all files seen!")
        student_id = delims[DELIM_WITH_STUDENTID]
        numb_efis_seen = 0
        print("----------------------FOR_STUDENT_" + student_id + "--------------------------------")

    if (functions.lower() in file.lower()):
        movefiles(file,functions)
    elif (sta.lower() in file.lower()):
        movefiles(file,sta)
    elif (stb.lower() in file.lower()):
        movefiles(file,stb)
    elif (st.lower() in file.lower()):
        movefiles(file,st)
    elif (stade.lower() in file.lower()):
        movefiles(file,stade)
    else:
        print( student_id + ": has bogus file "+file)

    #if got all 5 then compile and run
    if (numb_efis_seen == efis):
        out1 = open(script_output_results, "a")
        out1.write("----------------------START STUDENT_" + student_id + "--------------------------------\n\n\n")
        out1.close()

        clean_and_build()

        # run the process and capture its output
        cmds = "cd " + eclipse_proj_dir + ";cd ./Debug; ./327_Proj5"
        process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
        stdout, stderr = process.communicate(student_id)
        process.wait()

        out1 = open(script_output_results, "a")
        out1.write("----------------------END STUDENT_" + student_id + "--------------------------------\n\n\n")
        out1.close()

        # got em all, pause for tests
        # raw_input('     Press <ENTER> to continue')
out.close

