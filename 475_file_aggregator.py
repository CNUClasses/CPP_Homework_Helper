#get a list of files
from glob import glob
import shutil
import os
import subprocess
import sys
import errno

def findfile(start,name):
    '''

    :param start:
    :param name:
    :return:
    '''
    for relpath,dirs,files in os.walk(start, topdown=True):
        if name in files:
            return os.path.join(start,relpath,name)
    raise FileNotFoundError( errno.ENOENT, os.strerror(errno.ENOENT), start+name)

def Manage_files(where_student_files_are_dir, file_to_cpy, dest_dir, prefix):
    '''
    finds the main java file and copies it to a cheat directory to keep track of
    :param where_student_files_are_dir:
    :param file_to_cpy:
    :param dest_dir:
    :param prefix:  identifier
    :return:
    '''
    # get a list of student directories
    stud_dirs = glob(where_student_files_are_dir + "*")

    # where is student id
    stud_id_loc = len(where_student_files_are_dir.split("/"))-1

    for f in stud_dirs:
        try:
            f = findfile(f, file_to_cpy)
        except FileNotFoundError as e:
            print(e)
        else:
            studid = f.split("/")[stud_id_loc]
            newfiledir = dest_dir + prefix+ studid + "/"

            if not os.path.exists(newfiledir):
                os.mkdir(newfiledir)

            newfilename = newfiledir + prefix + file_to_cpy +".java"

            # copy file
            shutil.copy2(f, newfilename)
            # os.rename(f, newfilename)

dest_dir = "/home/keith/Desktop/475-575/proj2_cheat_new/"

where_student_files_are_dir =   "/home/keith/Desktop/475-575/proj2_cheat/"
file_to_cpy = "MainActivity.txt"
suffix = "-old"
Manage_files(where_student_files_are_dir,file_to_cpy,dest_dir, suffix)

where_student_files_are_dir =   "/home/keith/Desktop/475-575/s18_all/p2/p2_u/"
file_to_cpy = "MainActivity.java"
suffix = "-s18"
Manage_files(where_student_files_are_dir,file_to_cpy,dest_dir, suffix)

where_student_files_are_dir =   "/home/keith/Desktop/475-575/s19_all/p2/"
file_to_cpy = "MainActivity.java"
suffix = "-s19"
Manage_files(where_student_files_are_dir,file_to_cpy,dest_dir, suffix)


#
#
# for root, subdirs, files in os.walk(where_student_files_are_dir):
#
#     with open(where_student_files_are_dir, 'wb') as list_file:
#         for subdir in subdirs:
#             print('\t- subdirectory ' + subdir)
#
#         for filename in files:
#             file_path = os.path.join(root, filename)
#
#             print('\t- file %s (full path: %s)' % (filename, file_path))
#
# filelist = glob(where_student_files_are_dir,"MainActivity.*")
# # filelist.sort()
#
# def getFile(id, name = "joblist"):
#     for file in filelist:
#         if id in file:
#             if name in file:
#                 return file
#     return None
#
# #redirect output
# out = open(script_output_results,"w")
#
# # get a list of unique student ids
# studentids=set()
# for file in filelist:
#      delims = file.split("_")
#      studentids.add(delims[2])
# studentids = sorted(studentids)
#
# for id in studentids:
#
#     student_id = "----------------------FOR_STUDENT_" + id +"--------------------------------"
#     print(student_id)
#
#     # get the file to copy
#     stud_array_functions = getFile(id, "array_functions")
#     if stud_array_functions == None:
#         #either isnt there or caps problem
#         print("Student " + id + " failed to include array_functions.cpp")
#         continue
#     # else:
#     #     print(stud_array_functions)
#
#     # remove old files copy in new
#     cmds1 = "echo " + student_id + ";rm " + eclipse_project_dir + "array_functions.cpp"
#     cmds2 = "cp \"" + stud_array_functions +"\"  \"" + eclipse_project_dir + "array_functions.cpp\""
#
#     process = subprocess.Popen(cmds1, shell=True, stdout=out, stderr=out);
#     process.wait()
#     process = subprocess.Popen(cmds2, shell=True, stdout=out, stderr=out);
#     process.wait()
#
#     #clean
#     cmds = "cd " + eclipse_project_dir + ";cd ../Debug;make clean;"
#     process = subprocess.Popen(cmds, shell=True, stdout=out,stderr=out)
#     process.wait()
#
#     # build
#     cmds = "cd " + eclipse_project_dir + ";cd ../Debug;make;"
#     process = subprocess.Popen(cmds, shell=True, stdout=out,stderr=out)
#     process.wait()
#
#
#     #run the exe
#     cmds = "cd " + eclipse_project_dir + ";cd ..;./Debug/Project2_Solution.exe"
#     process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
#     process.wait()
#
#     pass
#
# out.close
#
