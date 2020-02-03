#get a list of files
from glob import glob
import os
import subprocess
import string

where_blackboard_files_are_dir = "/home/keith/Desktop/student_projects/327_projects/327proj1/f19/tmp/"
where_student_files_go = where_blackboard_files_are_dir + "repos/"

script_output_results = "327_Proj1.txt"
submission_filename = "submission.txt"
expected_files=['myfunc.h', 'myfunc.cpp', 'main.cpp', 'makefile']

# get a list of student files and lowercase them
filelist = glob(where_blackboard_files_are_dir + "*.txt")

def make_student_dir(id,base_path=where_student_files_go):
    '''
    create a directory for students work
    :param id:
    :param base_path:
    :return:
    '''
    pth = base_path + id
    try:
        os.mkdir(pth)
    except FileExistsError:
        print("OHNO " +str(id) +"directory exists! Shennanigans possible!")
        pass
    except Exception as ex:
        #handle all other exceptions
        print("OHNO " + str(id) + " Exception "+ ex)

    return pth

def getfile(id, name = submission_filename):
    '''
    grabs the student file that has the url
    :param id:
    :param name:
    :return:
    '''
    for file in filelist:
        if id in file:
            if name in file:
                return file
    return None

def run_cmd(cmd, pth):
    p = subprocess.Popen(cmd, cwd=pth, shell=True, stdout=out, stderr=out)
    grep_stdout = p.communicate()
    pass

def clear_rubbish_files(pth):
    '''
    dump all files not in expected_files
    :param pth:
    :return:
    '''
    root, dirs, files = next(os.walk(pth))
    intersection = set(expected_files).intersection(files)
    extras = set(files)-set(intersection)
    if( len(extras) > 0):
        print
    for extra in extras:
        tmp = root+ "/"+extra
        os.remove(root+ "/"+extra)

#redirect output
out = open(script_output_results,"w")

# get a list of unique student ids
studentids=set()
for file in filelist:
     delims = file.split("_")
     studentids.add(delims[3])
studentids = sorted(studentids)


def test_compile(cmd,projdir, myfle="myexe"):
    '''
    returns true if myexe exist after compiling
    :param cmd:
    :param projdir:
    :param info:
    :return:
    '''
    run_cmd(cmd, projdir)

    # if myexe exists then they never moved the function
    return os.path.exists(projdir + '/' + myfle)


for id in studentids:

    student_id = "----------------------FOR_STUDENT_" + id +"--------------------------------"
    print(student_id)
    git_url=None
    pth = None
    total = 100

    # get the file to get git URL from
    git_file = getfile(id,submission_filename)
    if git_file == None:
        #isn't there
        print("Student " + id + " failed to include a submission file")
        print("Total grade = 0")
        continue

    with open(git_file) as f:
        git_url = f.read()


    #clean it
    git_url = git_url.rstrip()
    git_url = git_url.split(' ')[-1]
    git_url=''.join((s if s in string.printable else'') for s in git_url)
    # git_url = str(filter(lambda x: x in string.printable, git_url))

    if git_url == None:
        # Aint there
        print("OHNO! Student, failed to include GIT URL in file!")
        print("Total grade = 0")
        continue

    #create student dir
    pth = make_student_dir(id,where_student_files_go)

    #clone directory
    cmd = "git clone " + git_url
    run_cmd(cmd,pth)

    # get the path of the project dir
    try:
        projdir = pth +"/"+ next(os.walk(pth))[1][0]
        print("Downloading from "+ git_url)
    except IndexError:
        print("OHNO! Failed to download project from "+ git_url)
        print("Total grade = 0")
        continue

    clear_rubbish_files(projdir)

    if (test_compile("g++ -o myexe main.cpp",projdir)):
        print("-20: never moved myfunc into myfunc.cpp ")
        total -=20

    if (not test_compile("g++ -o myexe main.cpp myfunc.cpp", projdir)):
        print("-20: does not compile")
        total -=20

    #run the exe

    # () run a subshell, change to the correct directory, run command, exit subshell
    cmd = "(cd " + projdir+ ";./myexe)"
    stdout_value = subprocess.getoutput(cmd)
    if( stdout_value.find("ello")==-1):
        print("-10: does not print hello world")
        total -= 10

    clear_rubbish_files(projdir)

    #see if make works
    if (not test_compile("make", projdir)):
        print("-20: make does not work")
        total -= 20

    #create at least one bogus file
    # run_cmd('touch bogus.o', projdir)
    if ( not os.path.exists(projdir+"/myfunc.o")):
        run_cmd('touch myfunc.o', projdir)
    if (test_compile("make clean", projdir, myfle="myfunc.o")):
        print("-20: make clean does not work correctly,did not remove all .o files")
        total -= 20

    print("Total grade ="+ str(total))


out.close

