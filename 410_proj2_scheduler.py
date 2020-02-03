#get a list of files
from glob import glob
import os
import subprocess
import sys

# CHANGE THESE
DELIM_WITH_STUDENTID=3
where_student_files_are_dir = "/home/keith/Desktop/student_projects/410/proj2_scheduler/dw/"
script_output_results = "410_proj2_scheduler_f19.txt"
# where to copy all the student files to test
eclipse_proj_dir= "/home/keith/git/410_proj2_scheduler_SOLUTION/"
executable = eclipse_proj_dir+'Debug/410_proj2_scheduler_SOLUTION'

# expected student files in submission
dispatcher      = "dispatcher.cpp"
stats           = "stats.cpp"
scheduler       = "scheduler.cpp"
scheduler_FIFO  = "scheduler_FIFO.cpp"
scheduler_RR    = "scheduler_RR.cpp"
scheduler_SRTF  = "scheduler_SRTF.cpp"

dispatcher_KP       = "dispatcher_KP"
stats_KP            = "stats_KP"
scheduler_KP        = "scheduler_KP"
scheduler_FIFO_KP   = "scheduler_FIFO_KP"
scheduler_RR_KP     = "scheduler_RR_KP"
scheduler_SRTF_KP   = "scheduler_SRTF_KP"

def clean_and_build_project():
    # clean
    cmds = "cd " + eclipse_proj_dir + ";cd ./Debug;make clean;"
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

    # build
    cmds = "cd " + eclipse_proj_dir + ";cd ./Debug;make;"
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

def remove_file(fn):
    # remove old file
    cmds = "rm " + fn
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

def movefile(dir, source_fle, dest_fle):
    global numb_efis_seen

    src_fle = os.path.join(os.path.join(eclipse_proj_dir, dir), source_fle)
    dst_fle = os.path.join(os.path.join(eclipse_proj_dir, dir), dest_fle)
    remove_file(dst_fle)
    copy_file(src_fle,dst_fle)

def copy_file(src_fle,dst_fle):
    # copy
    cmds = "cp \"" + src_fle + "\"  \"" + dst_fle + "\""
    process = subprocess.Popen(cmds, shell=True, stdout=out, stderr=out)
    process.wait()

def resetFiles():
    '''
    resets the project so its using MY 6 files
    :return:
    '''
    movefile("dispatcher",dispatcher_KP,dispatcher)
    movefile("stats",stats_KP,stats)
    movefile("scheduler", scheduler_KP, scheduler)
    movefile("scheduler", scheduler_FIFO_KP, scheduler_FIFO)
    movefile("scheduler", scheduler_RR_KP, scheduler_RR)
    movefile("scheduler", scheduler_SRTF_KP, scheduler_SRTF)

def get_student_file(filename,studentID):
    '''
    finds a file that has both the studentID and the filename of interest in its name(thanks shitty scholar)

    :param filename:
    :param studentID:
    :return:
    '''
    filelist = glob(where_student_files_are_dir + "*.cpp")
    filelist.sort()

    for fle in filelist:
        if studentID in fle:
            if filename in fle:
                return fle
    raise FileNotFoundError("student "+ studentID + " failed to submit "+ filename)

# get a list of student files
filelist = glob(where_student_files_are_dir + "*.cpp")
filelist.sort()

# get a list of unique student ids
studentids=set()
for file in filelist:
     delims = file.split("_")
     studentids.add(delims[DELIM_WITH_STUDENTID])
studentids = sorted(studentids)

#redirect output
out = open(script_output_results,"w")


# def run_exe_return_code(run_cmd):
#     process = subprocess.Popen(run_cmd + '; echo $?', stdout=subprocess.PIPE, shell=True)
#     (output, err) = process.communicate()
#     exit_code = process.wait()
#     return exit_code

def test_file(numb_points, id, fle, dir, fle2=None):
    resetFiles()    #start with correct solution
    print("Testing " + fle + ' for '+ str(numb_points)+' points' ,end=" ... ")
    try:
        stud_fle = get_student_file(fle, id)  # get the student file
        dest_file = os.path.join(os.path.join(eclipse_proj_dir, dir), fle)
        copy_file(stud_fle, dest_file)

        if(fle2 is not None):
            stud_fle = get_student_file(fle2, id)  # get the student file
            dest_file = os.path.join(os.path.join(eclipse_proj_dir, dir), fle2)
            copy_file(stud_fle, dest_file)


        clean_and_build_project()

        # lets see if we generated an executable
        if (os.path.exists(executable)):
            # run project and capture output
            cmd_out = "(cd " + eclipse_proj_dir + ";./Debug/410_proj2_scheduler_SOLUTION )"

            # run_exe_return_code(cmd_out)

            ret_code, stdout_value = subprocess.getstatusoutput(cmd_out)

            if (ret_code>9):
                if(ret_code == 139):
                    totpoints = numb_points // 2  # mercy points
                    print("ERROR!, segmentation fault! if for scheduler.cpp getNext(), did you check to see if the ready_q was empty first?... "+ str(totpoints) +" mercy points earned")
                    return totpoints
                else:
                    print ("ERROR!, ret_code ="+ str(ret_code))
            else:

                #so we need a point multiplier if 30 points then every failure counts off 3
                #if 20 points every failure counts off 2
                #if 15 or 10 every failure counts off 1
                mult = (numb_points//9)
                totpoints = numb_points-mult*ret_code

                print(str(totpoints)+' points earned!')
                return totpoints

        else:
             # my mistake for SRTF, REMOVE THIS FOR NEXT TIME
            if (fle == 'scheduler_SRTF.cpp'):
                totpoints = numb_points
                print(str(totpoints) + ' points earned!')
                return totpoints
            else:
                print("ERROR-probable compiler error in " + fle)


    except FileNotFoundError as err:
        print(err)
    except:
        print("Unexpected error:", sys.exc_info()[0])

    return 0


for id in studentids:
    print("----------------------FOR_STUDENT_" + id +"--------------------------------")

    grade = 5;

    # grade += test_file(20,id,stats,"stats")
    # grade += test_file(10, id, dispatcher, "dispatcher")
    # grade += test_file(30, id, scheduler, "scheduler")
    # grade += test_file(10, id, scheduler_FIFO, "scheduler",scheduler)
    grade += test_file(15, id, scheduler_SRTF, "scheduler",scheduler)
    grade += test_file(10, id, scheduler_RR, "scheduler",scheduler)

    print("student "+ id + " earned "+ str(grade))

out.close

