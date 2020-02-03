#get a list of files
from glob import glob
import os
import subprocess


# CHANGE THESE FILES
where_student_files_are_dir = '/home/keith/Desktop/student_projects/327_projects/327proj3/f19/s3/'
script_output_results = 'out_327_proj3_function_call_order.txt'
DELIM_WITH_STUDENTID=3

tmpdir = os.path.join(where_student_files_are_dir,'*.cpp')
filelist = glob(tmpdir )
filelist.sort()
def getFile(id, name ):
    for file in filelist:
        if id in file:
            if name in file:
                return file
    return None

#redirect output
out = open(script_output_results,'w')

# get a list of unique student ids
studentids=set()
for file in filelist:
     delims = file.split('_')
     studentids.add(delims[DELIM_WITH_STUDENTID])

studentids = sorted(studentids)

d = {'a':1,'b':2}
expected_order_library = ['void reloadAllData()',
                          'int checkout(int bookid',
                          'int checkin(int bookid)',
                          'int enroll(std::string &name)',
                          'int numbBooks()',
                          'int numbPatrons()',
                          'int howmanybooksdoesPatronHaveCheckedOut(int patronid)',
                          'int whatIsPatronName(std::string &name']
expected_order_fileio = ['int loadBooks(std::vector<book> &books',
                            'int saveBooks(std::vector<book> &books',
'int loadPatrons(std::vector<patron> &patrons',
'int savePatrons(std::vector<patron> &patrons']


def get_order_funcs(fle,vals):
    order_vals =[]
    with open(fle) as f:
        for line in f:
            for val in vals:
                if val in line:
                    order_vals.append(val)
    return order_vals


for id in studentids:

    student_id = '----------------------FOR_STUDENT_' + id +'--------------------------------'
    print(student_id)

    # get the 2 files to copy
    file_fileIO = getFile(id, 'fileIO')
    file_library = getFile(id, 'library')

    if (file_fileIO ==None):
        print('MISSING fileIO.cpp')
        continue

    if (file_library == None):
        print('MISSING library.cpp')
        continue

    order_library_vals =  get_order_funcs(file_library, expected_order_library)
    if (order_library_vals != expected_order_library):
         print("SUSPECT library")


    order_file_vals = get_order_funcs(file_fileIO, expected_order_fileio)
    if (order_file_vals != expected_order_fileio):
        print("SUSPECT fileio")


out.close

