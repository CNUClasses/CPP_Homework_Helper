#get a list of files
from glob import glob
import os
import subprocess
from subprocess import Popen, PIPE, STDOUT

where_blackboard_files_are_dir = "/home/keith/Desktop/Student Projects/327_projects/327proj1/f19/s1/"
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
     studentids.add(delims[2])
studentids = sorted(studentids)


def test_compile(cmd,projdir, myexe="myexe"):
    '''
    returns true if myexe exist after compiling
    :param cmd:
    :param projdir:
    :param info:
    :return:
    '''
    run_cmd(cmd, projdir)

    # if myexe exists then they never moved the function
    return os.path.exists(projdir + '/' + myexe)


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
        print("Student " + id + " failed to include file")
        continue

    with open(git_file) as f:
        git_url = f.read()

    #clean it
    git_url = git_url.rstrip()
    git_url = git_url.split(' ')[-1]

    if git_url == None:
        # Aint there
        print("Student " + id + " failed to include GIT URL in file")
        continue

    #create student dir
    pth = make_student_dir(id,where_student_files_go)

    # #clone directory
    # cmd = "git clone " + git_url
    # run_cmd(cmd,pth)

    # get the path of the project dir
    try:
        projdir = pth +"/"+ next(os.walk(pth))[1][0]
    except IndexError:
        print("OHNO " + str(id) + "Failed to download project from "+ git_url)
        continue

    clear_rubbish_files(projdir)

    if (test_compile("g++ -o myexe main.cpp",projdir)):
        print("-20: never moved myfunc into myfunc.cpp ")
        total -=20

    if (not test_compile("g++ -o myexe main.cpp myfunc.cpp", projdir)):
        print("-20: does not compile")
        total -=20

    #run the exe
    cmd = "./myexe"
    run_cmd(cmd,projdir)

    clear_rubbish_files(projdir)

    #see if make works
    if (not test_compile("make", projdir)):
        print("-20: make does not work")
        total -= 20

    #create at least one bogus file
    run_cmd('touch bogus.o', projdir)
    if (test_compile("make clean", projdir)):
        print("-20: make clean does not work")
        total -= 20



    print("Total grade ="+ str(total))


    #
    #
    #
    # #remove dispatcher.cpp and joblist.cpp
    # cmds1 = "echo " + student_id + ";rm " + dir_prog + "utilities.cpp"
    # cmds2 = "echo " + student_id + ";rm " + dir_prog + "results.txt"
    #
    # process = subprocess.Popen(cmds1, shell=True, stdout=out, stderr=out)
    # process.wait()
    # process = subprocess.Popen(cmds2, shell=True, stdout=out, stderr=out)
    # process.wait()
    #
    # #copy in 2 files (dispatcher and joblist)
    # cmds = "cp \"" + file_utilities +"\"  \"" + dir_prog + "utilities.cpp\""
    # process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    # process.wait()
    #
    #
    # #you can comment out the following lines, set a breakpoint on above process.wait
    # # then step through this program to breakpoint
    # # and then debug student code in eclipse
    #
    # #clean
    # cmds = "cd " + dir_prog + ";cd ./Debug;make clean;"
    # process = subprocess.Popen(cmds, shell=True, stdout=out,stderr=out)
    # process.wait()
    #
    # # build
    # cmds = "cd " + dir_prog + ";cd ./Debug;make;"
    # process = subprocess.Popen(cmds, shell=True, stdout=out,stderr=out)
    # process.wait()
    #
    #
    # #run the exe
    # cmds = "cd " + dir_prog + ";./Debug/Proj1_410_solution"
    # process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    # process.wait()
    #
    # pass
    #
    # # try:
    # #     # wanna see its output with 2 few params?
    # #     # subprocess.check_output([self.cmd_file, self.data_file, passfile])
    # #     print(subprocess.check_output([eclipse_exec]))
    # # except subprocess.CalledProcessError as err:
    # #     print("Problems...", "Utility returned:" + str(err.returncode) + " " + err.output)
    # # else:
    # #     print("No worries", "SUCCESS")


out.close

