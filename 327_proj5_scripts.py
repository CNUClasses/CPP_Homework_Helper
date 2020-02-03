#get a list of files
from glob import glob
import os
import subprocess
#import errno

# //where to copy all the student files
where_student_files_are_dir = "/home/keith/Desktop/327_projects/327_multithreaded_database/tmp/"

script_output_results = "327_stdouts_s19_p5.txt"

#make and clean here
proj       ="/home/keith/eclipse-workspace_MESSED_UP/MED_Tester/"
proj_debug ="/home/keith/eclipse-workspace_MESSED_UP/MED_Tester/Debug/"
datastore = "/home/keith/eclipse-workspace_MESSED_UP/datastore/"
datastore_dir = "/home/keith/eclipse-workspace_MESSED_UP/datastore/src/"
stringdatabase_dir = "/home/keith/eclipse-workspace_MESSED_UP/stringdatabase/src/"
stringdatabase = "/home/keith/eclipse-workspace_MESSED_UP/stringdatabase/"
crypto = "/home/keith/eclipse-workspace_MESSED_UP/crypto/"
MED_Tester_dir = "/home/keith/eclipse-workspace_MESSED_UP/MED_Tester/src/"
MED_Tester = "/home/keith/eclipse-workspace_MESSED_UP/MED_Tester/"
DELIM_WITH_STUDENTID=4

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
            print(e.args[1] + " " +filename)

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
    try:
        if(fn is None):
            return 0
        # copy in student files
        cmds = "cp \"" + fn + "\"  \"" + dest + "\""
        process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
        process.wait()
    except IOError as err:
        print("I/O error({0}): {1}".format(err))
        return 0
    else:
        # Success!
        return 1

def getFile(id, name, allfiles):
    for file in allfiles:
        if id in file:
            if name in file:
                return file

def getStudentIDs(filelist):
    # get a set of unique student ids
    studentids = set()
    for file in filelist:
        delims = file.split("_")
        studentids.add(delims[DELIM_WITH_STUDENTID])
    return sorted(studentids)


def clean_and_build(project_dir):
    global cmds, process
    cmds = "cd " + project_dir + ";cd ./Debug;make clean;make;"
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

def getfilelist(dirtosearch):
    # get a list of student files\
    filelist = glob(dirtosearch + "*.cpp")
    filelist.sort()
    return filelist

def writeToSTDOutput(data):
    cmds1 = "echo " + data
    process = subprocess.Popen(cmds1, shell=True, stdout=out, stderr=out);
    process.wait()

# ds = "data_store.cpp"
# dsf = "data_store_file.cpp"
# s_db = "string_database.cpp"
# MEDT = "MED_Tester.cpp"

def runAllProjects(*,files,IDs):
    #redirect output
    out = open(script_output_results,"w")
    EXPECTED_NUMBER_FILES = 3

    for ID in IDs:
        stud_ID = "----------------------FOR_STUDENT_" + ID + "--------------------------------"

        print(stud_ID)
        writeToSTDOutput(stud_ID)

        # get rid of last proj files
        deleterubbish()

        # get the 4 files to copy
        stud_ds = getFile(ID, ds, files)
        stud_dsf = getFile(ID, dsf, files)
        stud_s_db = getFile(ID, s_db, files)
        stud_MEDTest = getFile(ID, MEDT, files)

        #copy them
        numb_files_copied = 0
        numb_files_copied += movefile(stud_ds, os.path.join(datastore_dir, ds))
        numb_files_copied += movefile(stud_dsf, os.path.join(datastore_dir, dsf))
        numb_files_copied += movefile(stud_s_db, os.path.join(stringdatabase_dir, s_db))
        numb_files_copied += movefile(stud_MEDTest, os.path.join(MED_Tester_dir, "MED_Tester_STUDENT.txt"))

        if (numb_files_copied >= EXPECTED_NUMBER_FILES):
            #build the libraries first then the tester
            clean_and_build(crypto)
            clean_and_build(datastore)
            clean_and_build(stringdatabase)
            clean_and_build(MED_Tester)

            #NOTE THE FOLLOWING AUTORUNS PROGRAM BUT THERE IS A BUG WHERE COUT ISNT PRINTING TO LOG FILE
            # run the MED_tester and capture its output
            stud_ID = "----------------------RUNNING FOR_STUDENT_" + ID + "--------------------------------"
            cmds = "echo " + stud_ID
            process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
            process.wait(timeout=5)
            pass

            # cmds = "echo " + stud_ID+ ";cd " + MED_Tester + ";./Debug/MED_Tester "
            #
            # # # #give it a max of 5 seconds to run
            # process = subprocess.Popen(cmds,  shell=True, stdout=out, stderr=out)
            #
            # try:
            #     stud_ID = "----------------------RUNNING FOR_STUDENT_" + ID + "--------------------------------"
            #     process.wait(timeout=5)
            # except subprocess.TimeoutExpired:
            #     process.kill()
            #     print(stud_ID + "TIMEOUT DEADLOCK PROBABLE")
            #     writeToSTDOutput(stud_ID + "TIMEOUT DEADLOCK PROBABLE")


        else:
            print(f"Not enough files for {ID} expected {EXPECTED_NUMBER_FILES} got{numb_files_copied}")
        pass
if __name__=='__main__':

    #get all the files
    allfiles = getfilelist(where_student_files_are_dir)

    #get unique studentIDs
    studentIDs = getStudentIDs(allfiles)

    runAllProjects(files=allfiles,IDs = studentIDs)


