#get a list of files
from glob import glob
import os
import subprocess

# the parent directory where I'm running the eclipse C++ project
# eclipse_clean_dir = "/home/keith/eclipse-workspace/327_proj3_test/"
#
# /home/keith/eclipse-workspace/327_Proj4_Lib/includes
# /home/keith/eclipse-workspace/327_Proj4/

# //where to copy all the student files
eclipse_lib_dir= "/home/keith/eclipse-workspace/327_Proj5_Lib/"
where_student_files_are_dir = "/home/keith/Desktop/327_projects/327proj4/s18/"
script_output_results = "stdout_S18_327_P5.txt"

#make and clean here
proj ="/home/keith/eclipse-workspace/327_Proj5/Debug"
lib="/home/keith/eclipse-workspace/327_Proj5_Lib/Debug"
def make_and_clean():
    cmds = "cd " + lib + ";make clean;make;"
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

    cmds = "cd " + proj + ";make clean;make;"
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

# expected files in submission
proj4 = "327_Proj5" #will not copy to a cpp file so not compileable
functions = "Functions.cpp"
sta= "Smalltalk_American.cpp"
stb = "Smalltalk_Brit.cpp"
st = "Smalltalk.cpp"
stade = "ST_American_DonutEnthusiest.cpp"

efis = 6    # 6 for most
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
    if (numb_efis_seen == efis):
        make_and_clean()

        # run the process and capture its output
        cmds = "cd " + proj + ";./327_Proj5"
        process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
        stdout, stderr = process.communicate(student_id)
        process.wait()
        # got em all, pause for tests
        # raw_input('     Press <ENTER> to continue')

# get a list of student files
filelist = glob(where_student_files_are_dir + "*.cpp")
filelist.sort()

#redirect output
out = open(script_output_results,"w")
for file in filelist:
    global numb_efis_seen

    delimofinterest = 2

    delims = file.split("_")
    if(student_id != delims[delimofinterest]):
        if (numb_efis_seen !=efis  and len(student_id) !=0):
            print("   WARNING" + student_id + "not all files seen!")
        student_id = delims[delimofinterest]
        numb_efis_seen = 0
        print("----------------------FOR_STUDENT_" + student_id + "--------------------------------")

    if (functions in file):
        movefiles(file,functions)
    elif (sta in file):
        movefiles(file,sta)
    elif (stb in file):
        movefiles(file,stb)
    elif (st in file):
        movefiles(file,st)
    elif (stade in file):
        movefiles(file,stade)
    elif (proj4 in file):
        movefiles(file,proj4)
    elif (".txt" in file):
        pass
    else:
        print( student_id + ": has bogus file "+file)


    # # copy in student files
    # cmds = "cp \"" + file + "\"  \"" + stringparser_FQN+ "\""
    # process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    # process.wait()
    #
    # #you can comment out the following lines, set a breakpoint on above process.wait
    # # then step through this program to breakpoint
    # # and then debug student code in eclipse
    # # cmds = "cd " + eclipse_clean_dir + ";cd ./Debug;make clean;make all;"
    # # process = subprocess.Popen(cmds, shell=True, stdout=out,stderr=out)
    # # process.wait()

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

