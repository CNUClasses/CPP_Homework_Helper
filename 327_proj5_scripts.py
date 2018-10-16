#get a list of files
from glob import glob
import os
import subprocess
#import errno

# //where to copy all the student files
where_student_files_are_dir = "/home/keith/Desktop/327_projects/327_proj5/s18/"

script_output_results = "327_stdouts18_p5.txt"

#make and clean here
proj       ="/home/keith/eclipse-workspace/MED_Tester/"
proj_debug ="/home/keith/eclipse-workspace/MED_Tester/Debug/"
datastore_dir = "/home/keith/eclipse-workspace/datastore/src/"
stringdatabase_dir = "/home/keith/eclipse-workspace/stringdatabase/src/"
MED_Tester_dir = "/home/keith/eclipse-workspace/MED_Tester/src/"

ds = "data_store.cpp"
dsf = "data_store_file.cpp"
s_db = "string_database.cpp"
MEDT = "MED_Tester.cpp"

#redirect output
out = open(script_output_results,"w")

def make_and_clean():
    cmds = "cd " + proj_debug + ";make clean;make;"
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

def deleterubbish():
    def remove(filename):
        try:
            os.remove(filename)
        except OSError as e:  # this would be "except OSError, e:" before Python 2.6
            print(e.args)

    # get rid temps
    remove(os.path.join(proj,"Encryptfile1.txt"))
    remove(os.path.join(proj,"Encryptfile2.txt"))
    remove(os.path.join(proj,"noEncryptfile1.txt"))
    remove(os.path.join(proj,"noEncryptfile2.txt"))

    # and other student files
    remove(os.path.join(datastore_dir,ds))
    remove(os.path.join(datastore_dir,dsf))
    remove(os.path.join(stringdatabase_dir,s_db))
    remove(os.path.join(MED_Tester_dir,"MED_Tester_STUDENT.txt"))

efis = 4    # 6 for most
numb_efis_seen = 0
student_id = ''

def movefile(fn,dest):
    global numb_efis_seen,out

    # copy in student files
    cmds = "cp \"" + fn + "\"  \"" + dest + "\""
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

    print("     copied " + fn)

    # want to copy efis files and then pause to run diagnostics
    numb_efis_seen += 1
    if (numb_efis_seen == efis):
        numb_efis_seen = 0
        # make_and_clean()
        # got em all, pause for tests
        raw_input('     Press <ENTER> to continue')
        deleterubbish()

# ds = "data_store.cpp"
# dsf = "data_store_file.cpp"
# s_db = "string_database.cpp"
# MEDT = "MED_Tester.cpp"

def go_thru_files():
    # get a list of student files
    filelist = glob(where_student_files_are_dir + "*.cpp")
    filelist.sort()
    deleterubbish()

    #redirect output
    out = open(script_output_results,"w")
    for file in filelist:

        student_id = file.split("_")[3]
        if (numb_efis_seen == 0):
            print("----------------------FOR_STUDENT_" + student_id + "--------------------------------")


        if (ds in file):
            movefile(file,os.path.join(datastore_dir,ds))
        elif (dsf in file):
            movefile(file, os.path.join(datastore_dir, dsf))
        elif (s_db in file):
            movefile(file,os.path.join(stringdatabase_dir, s_db))
        elif (MEDT in file):
            movefile(file,os.path.join(MED_Tester_dir, "MED_Tester_STUDENT.txt"))
        else:
            print( student_id + ": has bogus file "+file)


out.close

if __name__=='__main__':
    go_thru_files()


