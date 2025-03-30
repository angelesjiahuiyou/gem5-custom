#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Tommaso Marinelli"
__email__  = "tommarin@ucm.es"

# Select the benchmark suite to use
# (allowed values: spec2006, spec2017)
benchsuite = "spec2017"

import argparse
from datetime import datetime, timedelta
import os
import platform
import shlex
import shutil
import sys
import time
import threading

python_version = float(".".join(map(str, sys.version_info[:2])))
if python_version < 3.2:
    import subprocess32 as subprocess
else:
    import subprocess

# Local modules
import simparams
try:
    if benchsuite == "spec2006":
        import benchsuites.spec2006 as benchlist
    elif benchsuite == "spec2017":
        import benchsuites.spec2017 as benchlist
    else:
        raise ImportError("Invalid benchmark suite")
except ImportError as error:
    print(error)
    exit(1)

uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])
home = os.path.expanduser("~")
bsyear = ''.join(c for c in benchsuite if c.isdigit())

# Total number of spawned processes
count_pids = 0
# Total number of failed processes
count_fail = 0
# Lock for processes list/counter update
lock_pids = threading.Lock()
# Lock for failed processes dict/counter update
lock_fail = threading.Lock()
# List of all the running subprocesses
sp_pids = []
# Dict which contains pending failed subprocesses with failure cause
sp_fail = {}
# Shutdown flag
shutdown = False


# Check if an executable is present in the current PATH
def cmd_exists(cmd):
    return any(
        os.access(os.path.join(path, cmd), os.X_OK)
        for path in os.environ["PATH"].split(os.pathsep)
    )


# Check for the presence of specific tools or paths in the system
def check_prerequisites(args, valgrind, simpoint, gem5, nvmain):
    exe_path = ""

    if valgrind:
        # Check if valgrind exists in current system
        if not cmd_exists("valgrind"):
            print("error: valgrind utility not found in env path")
            exit(2)

        # Check if the CPU architecture matches the execution platform
        machine = platform.machine()
        archs_aarch64 = ("aarch64_be", "aarch64", "armv8b", "armv8l", "arm64")
        archs_arm = ("arm", "armv7b", "armv7l", "armhf")
        archs_x86_64 = ("x86_64", "x64", "amd64")
        if ((args.arch == "aarch64" and machine not in archs_aarch64) or
            (args.arch == "armhf" and machine not in archs_arm) or
            (args.arch == "x86-64" and machine not in archs_x86_64)):
            print("error: architecture mismatch")
            exit(3)

    if simpoint:
        # Check if simpoint tool exists in specified path
        simpoint_exe = os.path.join(args.sp_dir, "bin", "simpoint")
        if not os.path.isfile(simpoint_exe):
            print("error: simpoint executable not found in " + args.sp_dir)
            exit(2)
        exe_path = simpoint_exe

    if gem5:
        # Check if gem5 exists in specified path
        gem5_build = "X86" if args.arch == "x86-64" else "ARM"
        gem5_exe_dir  = os.path.join(args.gem5_dir, "build", gem5_build)
        gem5_exe_name = "gem5.opt" if args.debug else "gem5.fast"
        gem5_exe_path = os.path.join(gem5_exe_dir, gem5_exe_name)
        if not os.path.isfile(gem5_exe_path):
            print("error: " + gem5_exe_name + " executable not found in " +
                  gem5_exe_dir)
            exit(2)
        exe_path = gem5_exe_path

    if nvmain:
        # Check if specified NVMAIN configuration file exists
        if args.mm_sim == "nvmain" and not os.path.isfile(args.nvmain_cfg):
            print("error: file " + args.nvmain_cfg + " not found")
            exit(2)
    return exe_path


# Get general benchmark parameters
def get_params(args, b_name):
    spec_b_folder = os.path.join(args.spec_dir, b_name)
    b_spl = b_name.split('.')

    # Check if the benchmark folder is present in SPEC path
    if not os.path.isdir(spec_b_folder):
        print("warning: " + b_name + " not found in " + args.spec_dir)
        return False, (None, None, None)

    # Check if the executable exists
    if b_name in benchlist.exe_name:
        b_exe_name = benchlist.exe_name[b_name] + "_base." + args.arch
    else:
        b_exe_name = b_spl[1] + "_base." + args.arch
    b_exe_folder = os.path.join(args.spec_dir, b_name, "exe")
    b_exe_path = os.path.join(b_exe_folder, b_exe_name)
    if not os.path.isfile(b_exe_path):
        print("warning: executable not found in " + b_exe_folder)
        return False, (None, None, None)

    b_preproc  = benchlist.preprocessing.get(b_name, "")
    # Use 2GB by default
    b_mem_size = "2GB"
    set_mem_size = benchlist.mem_size.get(args.set[0], "")
    if set_mem_size and set_mem_size.get(b_name, ""):
        b_mem_size = set_mem_size[b_name]
    arguments = (b_exe_name, b_preproc, b_mem_size)
    return True, arguments


# Get benchmark subset parameters
def get_ss_params(b_name, b_set):
    benchlist_subset = benchlist.subset.get(b_set)
    benchlist_params = benchlist.params.get(b_set)
    benchlist_input  = benchlist.input.get(b_set)
    if any(v is None for v in
        (benchlist_subset, benchlist_params, benchlist_input)):
        print("error: couldn't find benchmark set")
        exit(1)
    arguments = []
    b_params  = benchlist_params.get(b_name, "")
    b_input   = benchlist_input.get(b_name, "")
    if b_name in benchlist_subset:
        for i, ss in enumerate(benchlist_subset[b_name]):
            b_subset = ss + "_" + b_set
            arguments.append((b_subset,
                b_params[i] if isinstance(b_params, tuple) else "",
                b_input[i]  if isinstance(b_input, tuple) else ""))
    else:
        b_subset = b_set
        arguments.append((b_subset, b_params, b_input))
    return arguments


# Create a clone of the origin folder with symlinks to all the files
def mirror_dir(orig, dest):
    for root, dirs, files in os.walk(orig):
        subroot = root.split(orig + "/")[1] if root != orig else ""
        for name in dirs:
            os.mkdir(os.path.join(dest, subroot, name), 0o755)
        for name in files:
            os.symlink(os.path.join(root, name),
                os.path.join(dest, subroot, name))
    return


# Prepare the execution environment copying necessary files
def prepare_env(args, b_name, b_exe_name, b_preproc, target_dir):
    spec_b_folder = os.path.join(args.spec_dir, b_name)
    base_subfolder = os.path.join(args.arch, b_name)
    out_dir = os.path.join(args.out_dir, base_subfolder, target_dir)
    tmp_dir = os.path.join(out_dir, "tmp")

    # Remove the temporary folder if it already exists
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)

    # Create the temporary folder and consequently the output folder
    os.makedirs(tmp_dir, mode=0o755)

    # Make a symlink to the executable in the temporary directory
    b_exe_path = os.path.join(spec_b_folder, "exe", b_exe_name)
    os.symlink(b_exe_path, os.path.join(tmp_dir, b_exe_name))

    # Prepare the temporary directory with symlinks to input data
    b_set = args.set[0]
    if benchsuite == "spec2017":
        # If there's no data folder check in the rate benchmark folder
        if not os.path.isdir(os.path.join(spec_b_folder, "data")):
            rate_b_name = "5" + b_name[1:len(b_name)-1] + "r"
            spec_b_folder = os.path.join(args.spec_dir, rate_b_name)
        if b_set == "ref":
            if "_s" in b_name:
                # If there's no refspeed folder try with refrate
                b_set = ("refspeed" if os.path.isdir(os.path.join(
                    spec_b_folder, "data", "refspeed")) else "refrate")
            else:
                b_set = "refrate"

    input_folders = [os.path.join(spec_b_folder, "data", b_set, "input"),
        os.path.join(spec_b_folder, "data", "all", "input")]
    for d in input_folders:
        # Any invalid path will be ignored
        if os.path.isdir(d):
            mirror_dir(d, tmp_dir)

    # Do preprocessing of input data if necessary
    # TODO: remove "magic numbers"
    arch_bits = 64
    endianness = "le"

    cmd = benchlist.get_preprocessing(b_name, arch_bits, endianness)
    if cmd != None:
        proc = subprocess.Popen(cmd, shell=True, cwd=tmp_dir)
        proc.wait()

    return out_dir, tmp_dir


# Get host system memory utilization from /proc/meminfo
def get_host_mem():
    try:
        with open(os.path.join("/proc", "meminfo"), "r") as pidfile:
            stat = pidfile.readline()
            total = int(stat.split()[1])
            pidfile.readline()
            stat = pidfile.readline()
            avail = int(stat.split()[1])
            return(total, avail)
    except IOError:
        print("error: unable to read from /proc")
        exit(3)
    return 0


# Get process Resident Set Size (RSS) from /proc/[pid]/stat
def get_rss(pid):
    try:
        with open(os.path.join("/proc", str(pid), "stat"), 'r') as pidfile:
            stat = pidfile.readline()
            rss = int(stat.split(' ')[23])
            return rss
    except IOError:
        print("error: unable to read from /proc")
        exit(3)
    return 0


# Add a process to the failed list and update the counter
def fail(pid, cause):
    global count_fail
    global sp_fail

    with lock_fail:
        count_fail += 1
        sp_fail[pid] = cause
    print("PID " + str(pid) + " failed (code: " + cause + ")")
    return


# Watchdog which prevents host system memory saturation or process stall
def watchdog(limit_time):
    # Memory monitoring
    total, avail = get_host_mem()
    if float(avail) / float(total) < 0.1 and any(sp_pids):
        # Find the child which is using more memory
        largest_mem = [0, 0]
        for pid in sp_pids:
            # Avoid re-targeting a dead child
            proc_dir = os.path.join("/proc", str(pid))
            if pid not in sp_fail and os.path.isdir(proc_dir):
                mem = get_rss(pid)
                if mem > largest_mem[1]:
                    largest_mem[0] = pid
                    largest_mem[1] = mem
        if largest_mem[0] != 0:
            # Take note and kill it
            target = largest_mem[0]
            fail(target, "hostmem")
            os.kill(target, 9)
            # Wait some more time
            time.sleep(4)

    # Time monitoring
    current_time = datetime.now()
    if limit_time == True:
        for pid in sp_pids:
            # Avoid re-targeting a dead child
            proc_dir = os.path.join("/proc", str(pid))
            if pid not in sp_fail and os.path.isdir(proc_dir):
                limit = timedelta(hours = 6)
                ptime = datetime.fromtimestamp(os.path.getmtime(proc_dir))
                if current_time - ptime > limit:
                    # Take note and kill it
                    fail(pid, "timeout")
                    os.kill(pid, 9)
    return


# Spawn all the programs in the spawn list and control the execution
def execute(spawn_list, args, sem, limit_time=False):
    global shutdown

    # Create a thread for each child, to release the semaphore after execution
    # (this is needed because with subprocess it is only possible to wait for
    # a specific child to terminate, but we want to perform the operation when
    # ANY of them terminates, regardless of which one does)
    def run_in_thread(s):
        global count_pids
        global count_fail
        global sp_pids
        global sp_fail

        # Do not even execute if the program is turning off
        if shutdown:
            # Release the semaphore (allows dummy processing of other entries)
            sem.release()
            return

        cmd, in_name, work_path, logpath = s
        with open(logpath, "w") as logfile:
            if in_name:
                in_file = open(os.path.join(work_path, in_name), "rb", 0)
                proc = subprocess.Popen(cmd, cwd=work_path, stdin=in_file,
                    stdout=logfile, stderr=subprocess.STDOUT)
            else:
                proc = subprocess.Popen(cmd, cwd=work_path, stdout=logfile,
                    stderr=subprocess.STDOUT)
            pid = proc.pid
            with lock_pids:
                count_pids += 1
                sp_pids.append(pid)
            # Necessary: sometimes the thread is idling inside the routine
            if (shutdown and
                os.path.exists(os.path.join("/proc", str(pid)))):
                os.kill(pid, 9)
            proc.wait()
            # Flush internal buffers before closing the logfile
            logfile.flush()
            os.fsync(logfile.fileno())
            if in_name:
                in_file.close()

        if pid not in sp_fail and not shutdown:
            # Check logfile for known strings indicating a bad execution
            with open(logpath, "r") as logfile:
                log = logfile.read()
                if "fatal: Could not mmap" in log:
                    fail(pid, "alloc")
                elif "fatal: Out of memory" in log:
                    fail(pid, "oom")
                elif "fatal: Can't load checkpoint file" in log:
                    fail(pid, "parse")
                elif "fatal: syscall" in log:
                    fail(pid, "syscall")
                elif "panic: Unrecognized/invalid instruction" in log:
                    fail(pid, "instr")
                elif "panic: Tried to write unmapped address" in log:
                    fail(pid, "unmapad")
                elif "panic: Page table fault" in log:
                    fail(pid, "ptfault")
                elif "gem5 has encountered a segmentation fault!" in log:
                    fail(pid, "sigsegv")
                elif "Attempt to free invalid pointer" in log:
                    fail(pid, "invptr")
                elif "--- BEGIN LIBC BACKTRACE ---" in log:
                    fail(pid, "unknown")
                elif "Fortran runtime error" in log:
                    fail(pid, "fortran")
                elif ("Resuming from SimPoint" in log and
                        "Done running SimPoint!" not in log):
                    fail(pid, "incompl")

        # Directories cleanup / renaming
        work_dir = os.path.basename(work_path)
        out_path = (work_path if work_dir != "tmp" else uppath(work_path, 1))
        if not args.keep_tmp and shutdown:
            # It is useless to keep the output folder in case of brutal exit
            shutil.rmtree(out_path)
        else:
            # Move or rename relevant output files
            details = out_path.split('/')[-8:]
            sim_conf_id = (details[1].split('.')[0] + "_" +
                            details[0] + "_" +
                            details[3].replace("_", "") + "_" +
                            details[4].replace("-", "") + "_" +
                            details[5].replace("-", "") + "_" +
                            details[6].replace("-", "") + "_" +
                            ("cpt" + details[7].split('_')[1])
                             if "cpt" in out_path else "full")

            if out_path != work_path:
                wp_files = []
                if args.atrace:
                    wp_files.append(("access_trace.csv",
                                      sim_conf_id + "_accesses.csv"))
                if args.ctrace:
                    wp_files.append(("conflict_trace.csv",
                                      sim_conf_id + "_conflicts.csv"))
                    wp_files.append(("avoided_trace.csv",
                                      sim_conf_id + "_avoided.csv"))
                for f in wp_files:
                    if os.path.isfile(os.path.join(work_path, f[0])):
                        f_dest = f[1] if args.rename else f[0]
                        shutil.move(os.path.join(work_path, f[0]),
                                    os.path.join(out_path, f_dest))
            if (args.rename and
                os.path.isfile(os.path.join(out_path, "stats.txt"))):
                shutil.move(os.path.join(out_path, "stats.txt"),
                            os.path.join(out_path, sim_conf_id + "_stats.txt"))

            # Delete the temporary directory
            if work_dir == "tmp" and not args.keep_tmp:
                shutil.rmtree(work_path)
            if pid in sp_fail:
                # Rename directory indicating the cause of failure
                head, tail = os.path.split(out_path)
                dest_path = os.path.join(head,
                    "err_" + sp_fail[pid] + "_" + tail)
                if os.path.exists(dest_path):
                    shutil.rmtree(dest_path)
                os.rename(out_path, dest_path)
                # Clear the entry in the fail dict
                with lock_fail:
                    del sp_fail[pid]

        # Remove the process from the running list
        with lock_pids:
            sp_pids.remove(pid)

        # Release the semaphore (makes space for other processes)
        sem.release()
        return

    # The spawning procedure runs on a separate thread to avoid blocking
    # the main one (e.g. when the semaphore is waiting to be released)
    def spawn_in_thread():
        thread_list = []
        for s in spawn_list:
            # Acquire the semaphore (limits the number of active processes)
            sem.acquire()
            thread = threading.Thread(target=run_in_thread, args=(s,))
            thread_list.append(thread)
            thread.start()
        # Wait for all threads to terminate
        for t in thread_list:
            t.join()
        return

    # Main thread
    # Create and start the spawn thread
    spawn_thread = threading.Thread(target=spawn_in_thread)
    spawn_thread.start()

    try:
        # Periodically check resources utilization
        while(spawn_thread.is_alive()):
            if (not args.no_wd):
                watchdog(limit_time)
            time.sleep(1)
    except KeyboardInterrupt:
        # "Graceful" shutdown
        shutdown = True
        for pid in sp_pids:
            os.kill(pid, 9)
        exit(4)
    return


def bbv_gen(args, sem):
    spawn_list = []

    if not args.use_gem5:
        check_prerequisites(args, True, False, False, False)
    else:
        gem5_exe_path = check_prerequisites(args, False, False, True, False)

    print("BBV generation:")
    for b_name in args.benchmarks:
        print("- " + b_name)

        b_spl = b_name.split('.')
        b_abbr = b_spl[0] + b_spl[1]
        b_set = args.set[0]

        # Get benchmark general parameters from benchlist.py
        success, b_params = get_params(args, b_name)

        # Skip this benchmark if some error occurred
        if not success:
            continue

        b_exe_name = b_params[0]
        b_preproc  = b_params[1]
        b_mem_size = b_params[2]

        # Get benchmark subset parameters from benchlist.py
        ss_params = get_ss_params(b_name, b_set)

        for subset in ss_params:
            # Prepare the execution environment
            out_dir, tmp_dir = prepare_env(args, b_name, b_exe_name, b_preproc,
                os.path.join("bbv", subset[0]))

            bbv_filepath = os.path.join(out_dir, "bb2.out." + b_abbr + "." +
                subset[0])
            pc_filepath = os.path.join(out_dir, "pc2." + b_abbr + "." +
                subset[0])
            out_filepath = os.path.join(out_dir, b_abbr + "." + subset[0] +
                "2.out")
            log_filepath = os.path.join(out_dir, b_abbr + "." + subset[0] +
                "2.log")

            if not args.use_gem5:
                # Execute valgrind with exp-bbv tool
                cmd = ("valgrind --tool=exp-bbv --bb-out-file=" +
                    bbv_filepath + " --pc-out-file=" + pc_filepath + " ./" +
                    b_exe_name + " " + subset[1])
                in_name = subset[2]
            else:
                cmd = (gem5_exe_path + " --outdir=" + out_dir +
                    " " + os.path.join(args.gem5_dir, "configs", "example",
                    "se.py") + " --cpu-type=NonCachingSimpleCPU" +
                    " --simpoint-profile --simpoint-interval=" +
                    str(args.int_size) + " --output=" + out_filepath +
                    " --mem-size=" + b_mem_size +
                    " --cmd=./" + b_exe_name +
                    (" --options=\"" + subset[1] + "\"" if subset[1] else "") +
                    (" --input=" + subset[2] if subset[2] else ""))
                in_name = ""
            split_cmd = shlex.split(cmd)
            spawn_list.append((split_cmd, in_name, tmp_dir, log_filepath))

    execute(spawn_list, args, sem)
    return


def sp_gen(args, sem):
    spawn_list = []
    simpoint_exe = check_prerequisites(args, False, True, False, False)

    print("Simpoints generation:")
    for b_name in args.benchmarks:
        print("- " + b_name)

        base_subfolder = os.path.join(args.arch, b_name)
        b_spl = b_name.split('.')
        b_abbr = b_spl[0] + b_spl[1]
        b_set = args.set[0]

        # Get benchmark subset parameters from benchlist.py
        ss_params = get_ss_params(b_name, b_set)

        for subset in ss_params:
            out_dir = os.path.join(args.out_dir, base_subfolder, "simpoint",
                subset[0])
            data_dir = os.path.join(args.data_dir, base_subfolder, "bbv",
                subset[0])
            bbv_filename = "bb.out." + b_abbr + "." + subset[0]
            bbv_filepath = os.path.join(data_dir, bbv_filename)

            # Check if bbv files are present in the specified data directory
            if (not os.path.isfile(bbv_filepath)):
                print("warning: " + bbv_filename + " not found in " + data_dir)
                continue

            # Check if the bbv contains any interval
            rgx = subprocess.check_output("sed '/^[[:blank:]]*#/d;s/#.*//' " +
                bbv_filepath + " | wc -w", shell=True)
            result = int(rgx)
            if result == 0:
                print("warning: " + bbv_filename + " file does not contain " +
                    "any interval")
                continue

            # Create the output folder if not present
            if not os.path.isdir(out_dir):
                os.makedirs(out_dir, mode=0o755)

            sp_filepath = os.path.join(out_dir, "simpoint_" + subset[0])
            wgt_filepath = os.path.join(out_dir, "weight_" + subset[0])
            log_filepath = os.path.join(out_dir, "log_" + subset[0])

            # Execute the simpoint utility
            cmd = (simpoint_exe + " -loadFVFile " + bbv_filepath + " -maxK " +
                str(args.maxk) + " -saveSimpoints " + sp_filepath +
                " -saveSimpointWeights " + wgt_filepath)
            in_name = ""
            split_cmd = shlex.split(cmd)
            spawn_list.append((split_cmd, in_name, out_dir, log_filepath))

    execute(spawn_list, args, sem)
    return


def cp_gen(args, sem):
    spawn_list = []
    gem5_exe_path = check_prerequisites(args, False, False, True, False)

    print("Checkpoints generation:")
    for b_name in args.benchmarks:
        print("- " + b_name)

        base_subfolder = os.path.join(args.arch, b_name)
        b_spl = b_name.split('.')
        b_abbr = b_spl[0] + b_spl[1]
        b_set = args.set[0]

        # Get benchmark general parameters from benchlist.py
        success, b_params = get_params(args, b_name)

        # Skip this benchmark if some error occurred
        if not success:
            continue

        b_exe_name = b_params[0]
        b_preproc  = b_params[1]
        b_mem_size = b_params[2]

        # Get benchmark subset parameters from benchlist.py
        ss_params = get_ss_params(b_name, b_set)

        for subset in ss_params:
            data_dir = os.path.join(args.data_dir, base_subfolder, "simpoint",
                subset[0])
            sp_filename = "simpoint_" + subset[0]
            wgt_filename = "weight_" + subset[0]
            sp_filepath = os.path.join(data_dir, sp_filename)
            wgt_filepath = os.path.join(data_dir, wgt_filename)

            # Check if simpoints are present in the specified data directory
            if (not os.path.isfile(sp_filepath)):
                print("warning: " + sp_filename + " not found in " + data_dir)
                continue
            elif (not os.path.isfile(wgt_filepath)):
                print("warning: " + wgt_filename + " not found in " + data_dir)
                continue

            out_dir, tmp_dir = prepare_env(args, b_name, b_exe_name, b_preproc,
                os.path.join("checkpoint", subset[0]))

            out_filepath = os.path.join(out_dir, b_abbr + ".out")
            log_filepath = os.path.join(out_dir, "gem5." + b_abbr + ".out")

            cmd = (gem5_exe_path + " --outdir=" + out_dir + " " +
                os.path.join(args.gem5_dir, "configs", "example", "se.py") +
                " --cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=" +
                sp_filepath + "," + wgt_filepath + "," + str(args.int_size) +
                "," + str(args.warmup) + " --output=" + out_filepath +
                " --mem-size=" + b_mem_size +
                " --cmd=./" + b_exe_name + (" --options=\"" + subset[1] + "\""
                if subset[1] else "") + (" --input=" + subset[2] if subset[2]
                else ""))
            in_name = ""
            split_cmd = shlex.split(cmd)
            spawn_list.append((split_cmd, in_name, tmp_dir, log_filepath))

    execute(spawn_list, args, sem)
    return


def cp_sim(args, sem):
    spawn_list = []
    gem5_exe_path = check_prerequisites(args, False, False, True, True)

    print("Benchmark simulation from checkpoints:")
    for b_name in args.benchmarks:
        print("- " + b_name)

        base_subfolder = os.path.join(args.arch, b_name)
        data_dir = os.path.join(args.data_dir, base_subfolder, "checkpoint")
        b_spl = b_name.split('.')
        b_abbr = b_spl[0] + b_spl[1]
        b_set = args.set[0]

        # Get benchmark general parameters from benchlist.py
        success, b_params = get_params(args, b_name)

        # Skip this benchmark if some error occurred
        if not success:
            continue

        b_exe_name = b_params[0]
        b_preproc  = b_params[1]
        b_mem_size = b_params[2]

        # Get benchmark subset parameters from benchlist.py
        ss_params = get_ss_params(b_name, b_set)

        for subset in ss_params:
            data_ss_dir = data_dir + "/" + subset[0]
            cpt_prefix = "cpt.simpoint_"

            # Check if checkpoints are present in the specified data directory
            if (not os.path.isdir(data_ss_dir)):
                print("warning: directory " + data_ss_dir + " not found")
                continue
            cpt_folders = (
                sorted([d for d in os.listdir(data_ss_dir) if cpt_prefix in d],
                key=lambda x: float(x.split('_')[5]), reverse=True)
            )
            if (not any(cpt_folders)):
                print("warning: no checkpoints found in " + data_ss_dir)
                continue
            if args.cpts and args.cpts < len(cpt_folders):
                cpt_folders = cpt_folders[:args.cpts]

            # Select CPU architecture and corresponding parameters
            cpu = []
            for model in simparams.cpu_models[args.arch]:
                cpu.append((model, simparams.cpu_models[args.arch][model]))

            # Simulate all possible cases (can be a lot!)
            instances = [(model, tech, case, cpt) for model in cpu
                for tech in simparams.mem_technologies.get(
                    model[0], simparams.mem_technologies.get("default"))
                for case in simparams.mem_cases.get(
                    tech, simparams.mem_cases.get("default"))
                for cpt in cpt_folders]
            for i in instances:
                model = i[0]
                tech  = i[1]
                case  = i[2]
                cpt   = i[3]

                model_name = model[0]
                model_cpu, model_conf, model_volt, model_freq = model[1]
                dict_mn = (model_name
                    if model_name in simparams.mem_technologies else "default")
                hier  = simparams.mem_technologies[dict_mn][tech]

                out_dir, tmp_dir = prepare_env(args, b_name, b_exe_name,
                    b_preproc, os.path.join("simulation", subset[0],
                    model_name, tech, case, cpt))

                out_filepath = os.path.join(out_dir, b_abbr + ".out")
                log_filepath = os.path.join(out_dir, "gem5." + b_abbr + ".out")
                nstats_filepath = os.path.join(out_dir, "nvmain_stats." +
                    b_abbr + ".log")
                nconf_filepath = os.path.join(out_dir, "nvmain_config." +
                    b_abbr + ".log")

                cache = simparams.mem_configs[model_name]
                l1ip = simparams.hwp_config.get(args.l1i_hwp, "")
                l1dp = simparams.hwp_config.get(args.l1d_hwp, "")
                l2p = simparams.hwp_config.get(args.l2_hwp, "")
                l3p = simparams.hwp_config.get(args.l3_hwp, "")
                cmd = (gem5_exe_path +
                    (" --debug-flags=AccessTrace" if args.atrace else "") +
                    (" --debug-flags=ConflictTrace" if args.ctrace else "") +
                    " --outdir=" + out_dir +
                    " " + os.path.join(args.gem5_dir, "configs", "example",
                    model_conf) +
                    " --hwp-override" +
                    " --caches" +
                    (" --l1d-hwp-type=" + str(l1dp[0]) +
                        (" --l1d-hwp-deg=" + str(l1dp[1]) if l1dp[1] else "") +
                        (" --l1d-hwp-lat=" + str(l1dp[2]) if l1dp[2] else "") +
                        (" --l1d-hwp-qs=" +  str(l1dp[3]) if l1dp[3] else "")
                        if l1dp else "") +
                    " --l1d-data-lat=" +  str(cache[hier[0]][case][0][0]) +
                    " --l1d-write-lat=" + str(cache[hier[0]][case][0][1]) +
                    " --l1d-tag-lat=" +   str(cache[hier[0]][case][0][2]) +
                    " --l1d-resp-lat=" +  str(cache[hier[0]][case][0][3]) +
                    " --l1d_size=" +      str(cache[hier[0]][case][0][4]) +
                    " --l1d_assoc=" +     str(cache[hier[0]][case][0][5]) +
                    (" --l1i-hwp-type=" + str(l1ip[0]) +
                        (" --l1i-hwp-deg=" + str(l1ip[1]) if l1ip[1] else "") +
                        (" --l1i-hwp-lat=" + str(l1ip[2]) if l1ip[2] else "") +
                        (" --l1i-hwp-qs=" +  str(l1ip[3]) if l1ip[3] else "")
                        if l1ip else "") +
                    " --l1i-data-lat=" +  str(cache[hier[1]][case][1][0]) +
                    " --l1i-write-lat=" + str(cache[hier[1]][case][1][1]) +
                    " --l1i-tag-lat=" +   str(cache[hier[1]][case][1][2]) +
                    " --l1i-resp-lat=" +  str(cache[hier[1]][case][1][3]) +
                    " --l1i_size=" +      str(cache[hier[1]][case][1][4]) +
                    " --l1i_assoc=" +     str(cache[hier[1]][case][1][5]) +
                    " --l2cache" +
                    (" --l2-enable-banks --l2-num-banks=" + str(args.l2_banks)
                        if args.l2_banks else "") +
                    (" --l2-hwp-type=" + str(l2p[0]) +
                        (" --l2-hwp-deg=" + str(l2p[1]) if l2p[1] else "") +
                        (" --l2-hwp-lat=" + str(l2p[2]) if l2p[2] else "") +
                        (" --l2-hwp-qs=" +  str(l2p[3]) if l2p[3] else "")
                        if l2p else "") +
                    " --l2-data-lat=" +   str(cache[hier[2]][case][2][0]) +
                    " --l2-write-lat=" +  str(cache[hier[2]][case][2][1]) +
                    " --l2-tag-lat=" +    str(cache[hier[2]][case][2][2]) +
                    " --l2-resp-lat=" +   str(cache[hier[2]][case][2][3]) +
                    " --l2_size=" +       str(cache[hier[2]][case][2][4]) +
                    " --l2_assoc=" +      str(cache[hier[2]][case][2][5]) +
                    (" --l3cache " +
                    (" --l3-enable-banks --l3-num-banks=" + str(args.l3_banks)
                        if args.l3_banks else "") +
                    (" --l3-hwp-type=" + str(l3p[0]) +
                        (" --l3-hwp-deg=" + str(l3p[1]) if l3p[1] else "") +
                        (" --l3-hwp-lat=" + str(l3p[2]) if l3p[2] else "") +
                        (" --l3-hwp-qs=" +  str(l3p[3]) if l3p[3] else "")
                        if l3p else "") +
                    " --l3-data-lat=" +   str(cache[hier[3]][case][3][0]) +
                    " --l3-write-lat=" +  str(cache[hier[3]][case][3][1]) +
                    " --l3-tag-lat=" +    str(cache[hier[3]][case][3][2]) +
                    " --l3-resp-lat=" +   str(cache[hier[3]][case][3][3]) +
                    " --l3_size=" +       str(cache[hier[3]][case][3][4]) +
                    " --l3_assoc=" +      str(cache[hier[3]][case][3][5])
                    if hier[3] != "none" else "") +
                    " --num-cpus=1" +
                    " --cpu-type=" + model_cpu +
                    " --cpu-clock=" + model_freq +
                    " --cpu-voltage=" + model_volt +
                    " --sys-clock=\"1.2GHz\"" +
                    " --sys-voltage=\"1.2V\"" +
                    " --restore-simpoint-checkpoint"
                    " --checkpoint-dir=" + data_ss_dir +
                    " --checkpoint-restore=" + str(cpt_folders.index(cpt)+1) +
                    " --output=" + out_filepath +
                    " --mem-size=" + b_mem_size +
                    " --cmd=./" + b_exe_name +
                    (" --options=\"" + subset[1] + "\"" if subset[1] else "") +
                    (" --input=" + subset[2] if subset[2] else "") +
                    " --mem-type=" + ("NVMainMemory" +
                    " --nvmain-config=" + args.nvmain_cfg +
                    " --nvmain-StatsFile=" + nstats_filepath +
                    " --nvmain-ConfigLog=" + nconf_filepath
                    if args.mm_sim == "nvmain" else "DDR4_2400_8x8"))
                in_name = ""
                split_cmd = shlex.split(cmd)
                spawn_list.append((split_cmd, in_name, tmp_dir, log_filepath))

    execute(spawn_list, args, sem, True)
    return


def full_sim(args, sem):
    spawn_list = []
    gem5_exe_path = check_prerequisites(args, False, False, True, True)

    print("Full benchmark simulation:")
    for b_name in args.benchmarks:
        print("- " + b_name)

        b_spl = b_name.split('.')
        b_abbr = b_spl[0] + b_spl[1]
        b_set = args.set[0]

        # Get benchmark general parameters from benchlist.py
        success, b_params = get_params(args, b_name)

        # Skip this benchmark if some error occurred
        if not success:
            continue

        b_exe_name = b_params[0]
        b_preproc  = b_params[1]
        b_mem_size = b_params[2]

        # Get benchmark subset parameters from benchlist.py
        ss_params = get_ss_params(b_name, b_set)

        for subset in ss_params:

            # Select CPU architecture and corresponding parameters
            cpu = []
            for model in simparams.cpu_models[args.arch]:
                cpu.append((model, simparams.cpu_models[args.arch][model]))

            # Simulate all possible cases
            instances = [(model, tech, case) for model in cpu
                for tech in simparams.mem_technologies.get(
                    model[0], simparams.mem_technologies.get("default"))
                for case in simparams.mem_cases.get(
                    tech, simparams.mem_cases.get("default"))]
            for i in instances:
                model = i[0]
                tech  = i[1]
                case  = i[2]

                model_name = model[0]
                model_cpu, model_conf, model_volt, model_freq = model[1]
                dict_mn = (model_name
                    if model_name in simparams.mem_technologies else "default")
                hier  = simparams.mem_technologies[dict_mn][tech]

                out_dir, tmp_dir = prepare_env(args, b_name, b_exe_name,
                    b_preproc, os.path.join("simulation", subset[0],
                    model_name, tech, case, "full"))

                out_filepath = os.path.join(out_dir, b_abbr + ".out")
                log_filepath = os.path.join(out_dir, "gem5." + b_abbr + ".out")
                nstats_filepath = os.path.join(out_dir, "nvmain_stats." +
                    b_abbr + ".log")
                nconf_filepath = os.path.join(out_dir, "nvmain_config." +
                    b_abbr + ".log")

                cache = simparams.mem_configs[model_name]
                l1ip = simparams.hwp_config.get(args.l1i_hwp, "")
                l1dp = simparams.hwp_config.get(args.l1d_hwp, "")
                l2p = simparams.hwp_config.get(args.l2_hwp, "")
                l3p = simparams.hwp_config.get(args.l3_hwp, "")
                cmd = (gem5_exe_path +
                    (" --debug-flags=AccessTrace" if args.atrace else "") +
                    (" --debug-flags=ConflictTrace" if args.ctrace else "") +
                    " --outdir=" + out_dir +
                    " " + os.path.join(args.gem5_dir, "configs", "example",
                    model_conf) +
                    " --hwp-override" +
                    " --caches" +
                    (" --l1d-hwp-type=" + str(l1dp[0]) +
                        (" --l1d-hwp-deg=" + str(l1dp[1]) if l1dp[1] else "") +
                        (" --l1d-hwp-lat=" + str(l1dp[2]) if l1dp[2] else "") +
                        (" --l1d-hwp-qs=" +  str(l1dp[3]) if l1dp[3] else "")
                        if l1dp else "") +
                    " --l1d-data-lat=" +  str(cache[hier[0]][case][0][0]) +
                    " --l1d-write-lat=" + str(cache[hier[0]][case][0][1]) +
                    " --l1d-tag-lat=" +   str(cache[hier[0]][case][0][2]) +
                    " --l1d-resp-lat=" +  str(cache[hier[0]][case][0][3]) +
                    " --l1d_size=" +      str(cache[hier[0]][case][0][4]) +
                    " --l1d_assoc=" +     str(cache[hier[0]][case][0][5]) +
                    (" --l1i-hwp-type=" + str(l1ip[0]) +
                        (" --l1i-hwp-deg=" + str(l1ip[1]) if l1ip[1] else "") +
                        (" --l1i-hwp-lat=" + str(l1ip[2]) if l1ip[2] else "") +
                        (" --l1i-hwp-qs=" +  str(l1ip[3]) if l1ip[3] else "")
                        if l1ip else "") +
                    " --l1i-data-lat=" +  str(cache[hier[1]][case][1][0]) +
                    " --l1i-write-lat=" + str(cache[hier[1]][case][1][1]) +
                    " --l1i-tag-lat=" +   str(cache[hier[1]][case][1][2]) +
                    " --l1i-resp-lat=" +  str(cache[hier[1]][case][1][3]) +
                    " --l1i_size=" +      str(cache[hier[1]][case][1][4]) +
                    " --l1i_assoc=" +     str(cache[hier[1]][case][1][5]) +
                    " --l2cache" +
                    (" --l2-enable-banks --l2-num-banks=" + str(args.l2_banks)
                        if args.l2_banks else "") +
                    (" --l2-hwp-type=" + str(l2p[0]) +
                        (" --l2-hwp-deg=" + str(l2p[1]) if l2p[1] else "") +
                        (" --l2-hwp-lat=" + str(l2p[2]) if l2p[2] else "") +
                        (" --l2-hwp-qs=" +  str(l2p[3]) if l2p[3] else "")
                        if l2p else "") +
                    " --l2-data-lat=" +   str(cache[hier[2]][case][2][0]) +
                    " --l2-write-lat=" +  str(cache[hier[2]][case][2][1]) +
                    " --l2-tag-lat=" +    str(cache[hier[2]][case][2][2]) +
                    " --l2-resp-lat=" +   str(cache[hier[2]][case][2][3]) +
                    " --l2_size=" +       str(cache[hier[2]][case][2][4]) +
                    " --l2_assoc=" +      str(cache[hier[2]][case][2][5]) +
                    (" --l3cache " +
                    (" --l3-enable-banks --l3-num-banks=" + str(args.l3_banks)
                        if args.l3_banks else "") +
                    (" --l3-hwp-type=" + str(l3p[0]) +
                        (" --l3-hwp-deg=" + str(l3p[1]) if l3p[1] else "") +
                        (" --l3-hwp-lat=" + str(l3p[2]) if l3p[2] else "") +
                        (" --l3-hwp-qs=" +  str(l3p[3]) if l3p[3] else "")
                        if l3p else "") +
                    " --l3-data-lat=" +   str(cache[hier[3]][case][3][0]) +
                    " --l3-write-lat=" +  str(cache[hier[3]][case][3][1]) +
                    " --l3-tag-lat=" +    str(cache[hier[3]][case][3][2]) +
                    " --l3-resp-lat=" +   str(cache[hier[3]][case][3][3]) +
                    " --l3_size=" +       str(cache[hier[3]][case][3][4]) +
                    " --l3_assoc=" +      str(cache[hier[3]][case][3][5])
                    if hier[3] != "none" else "") +
                    " --num-cpus=1" +
                    " --cpu-type=" + model_cpu +
                    " --cpu-clock=" + model_freq +
                    " --cpu-voltage=" + model_volt +
                    " --sys-clock=\"1.2GHz\"" +
                    " --sys-voltage=\"1.2V\"" +
                    " --output=" + out_filepath +
                    " --mem-size=" + b_mem_size +
                    " --cmd=./" + b_exe_name +
                    (" --options=\"" + subset[1] + "\"" if subset[1] else "") +
                    (" --input=" + subset[2] if subset[2] else "") +
                    " --mem-type=" + ("NVMainMemory" +
                    " --nvmain-config=" + args.nvmain_cfg +
                    " --nvmain-StatsFile=" + nstats_filepath +
                    " --nvmain-ConfigLog=" + nconf_filepath
                    if args.mm_sim == "nvmain" else "DDR4_2400_8x8"))
                in_name = ""
                split_cmd = shlex.split(cmd)
                spawn_list.append((split_cmd, in_name, tmp_dir, log_filepath))

    execute(spawn_list, args, sem)
    return


def profile(args, sem):
    spawn_list = []
    check_prerequisites(args, True, False, False, False)

    print("Memory profiling:")
    for b_name in args.benchmarks:
        print("- " + b_name)

        b_spl = b_name.split('.')
        b_abbr = b_spl[0] + b_spl[1]
        b_set = args.set[0]

        # Get benchmark general parameters from benchlist.py
        success, b_params = get_params(args, b_name)

        # Skip this benchmark if some error occurred
        if not success:
            continue

        b_exe_name = b_params[0]
        b_preproc  = b_params[1]

        # Get benchmark subset parameters from benchlist.py
        ss_params = get_ss_params(b_name, b_set)

        for subset in ss_params:
            # Prepare the execution environment
            out_dir, tmp_dir = prepare_env(args, b_name, b_exe_name, b_preproc,
                os.path.join("profile", subset[0]))

            mem_filepath = os.path.join(out_dir, "mem." + b_abbr + "." +
                subset[0])
            log_filepath = os.path.join(out_dir, b_abbr + "." + subset[0] +
                ".log")

            # Execute valgrind with massif tool
            cmd = ("valgrind --tool=massif --pages-as-heap=yes" +
                " --massif-out-file=" + mem_filepath + " ./" +
                b_exe_name + " " + subset[1])
            in_name = subset[2]
            split_cmd = shlex.split(cmd)
            spawn_list.append((split_cmd, in_name, tmp_dir, log_filepath))

    execute(spawn_list, args, sem)
    return

def counters(args, sem):
    spawn_list = []
#    check_prerequisites(args, True, False, False, False)

    print("Hardware counters:")
    for b_name in args.benchmarks:
 #       print("- " + b_name)

        b_spl = b_name.split('.')
        b_abbr = b_spl[0] + b_spl[1]
        b_set = args.set[0]

        # Get benchmark general parameters from benchlist.py
        success, b_params = get_params(args, b_name)

        # Skip this benchmark if some error occurred
        if not success:
            continue

        b_exe_name = b_params[0]
        b_preproc  = b_params[1]
  #      print(b_exe_name)

        # Get benchmark subset parameters from benchlist.py
        ss_params = get_ss_params(b_name, b_set)

        if args.sss:
                # Take first subset only
                ss_params = ss_params[:1]


        for subset in ss_params:
#            print(subset[1])
            # Prepare the execution environment
            out_dir, tmp_dir = prepare_env(args, b_name, b_exe_name, b_preproc,
                os.path.join("counter", subset[0]))

            mem_filepath = os.path.join(out_dir, "mem." + b_abbr + "." +
                subset[0])
            log_filepath = os.path.join(out_dir, b_abbr + "." + subset[0] +
                   "stat_full6_05sperf.log")                #"stat_sampling6_1ms_21perf.log")
            perf_data_file = os.path.join(out_dir, b_abbr + "." + subset[0] +
                    "perf_data_sampling_instructions_100000000_test2.data")

            # Execute perf (instead of perf stat, perf record)
#            cmd = ("perf record -e duration_time -e armv8_pmuv3_0/cpu_cycles/ " +
            cmd = ("perf stat " +  # not parsing
########****parsing            cmd = ("perf stat -I 1 " + #-e instructions "+ ## cpu-cycles -e instructions " +
##            cmd = ("perf record -e instructions -c 100000000 " +#-e duration_time -e armv8_pmuv3_0/cpu_cycles/ " +
#                    "-e armv8_pmuv3_0/exc_return/ 
  ##                   "-e armv8_pmuv3_0/l1d_cache/ " +
##                    "-e armv8_pmuv3_0/l1i_cache/ " + 
#                     "-e armv8_pmuv3_0/l2d_cache/ " +
 #                    "-e armv8_pmuv3_0/l2i_cache/ " +
                     "-e cpu-cycles " +
##                     "-e armv8_pmuv3_0/ll_cache/ -e l2d_cache_rd " +
#######                     "-e armv8_pmuv3_0/ll_cache_miss/ " +  "-e armv8_pmuv3_0/mem_access/ " +
    #                "-e l1d_cache_rd -e l2d_cache_rd " + #"-e uncore_hisi_l3c.rd_cpipe " +
                    #"-e uncore_hisi_l3c.wr_cpipe 
     #               "-e cpu-cycles -e instructions " +
      #              "-e branch-misses -e bus-cycles
      #               "-e cache-misses " +
       #             "-e cache-references -e cpu-cycles -e cycles -e instructions " +
        #            "-e stalled-cycles-backend -e idle-cycles-backend " +
         #           "-e stalled-cycles-frontend -e idle-cycles-frontend " +
          #          "-e alignment-faults -e bpf-output -e context-switches " +
           #         "-e cpu-clock -e cpu-migrations -e dummy -e emulation-faults " +
            #        "-e major-faults -e minor-faults -e page-faults " +
             #       "-e task-clock -e duration_time -e L1-dcache-load-misses " +
              #      "-e L1-dcache-loads -e L1-icache-load-misses -e L1-icache-loads " +
               #     "-e branch-load-misses -e branch-loads -e dTLB-load-misses " +
                #    "-e dTLB-loads -e iTLB-load-misses -e iTLB-loads " +
                 #   "-e armv8_pmuv3_0/br_mis_pred/ -e armv8_pmuv3_0/br_mis_pred_retired/ " +
                  #  "-e armv8_pmuv3_0/br_pred/ -e armv8_pmuv3_0/br_retired/ " +
                   # "-e armv8_pmuv3_0/br_return_retired/ -e armv8_pmuv3_0/bus_access/ " +
                    #"-e armv8_pmuv3_0/bus_cycles/ -e armv8_pmuv3_0/cid_write_retired/ " +
#                    "-e armv8_pmuv3_0/cpu_cycles/ -e  armv8_pmuv3_0/dtlb_walk/ " +
 #                   "-e armv8_pmuv3_0/exc_return/ -e armv8_pmuv3_0/exc_taken/ " +
                     "-e armv8_pmuv3_0/inst_retired/ " +#-e armv8_pmuv3_0/inst_spec/ " +
   #                 "-e armv8_pmuv3_0/itlb_walk/ -e armv8_pmuv3_0/l1d_cache/ " +
                    "-e armv8_pmuv3_0/l1d_cache_refill/ " + # -e armv8_pmuv3_0/l1d_cache_wb/ " +
     #               "-e armv8_pmuv3_0/l1d_tlb/ -e armv8_pmuv3_0/l1d_tlb_refill/ " +
      #              "-e armv8_pmuv3_0/l1i_cache/ 
                    "-e armv8_pmuv3_0/l1i_cache_refill/ " +
       #             "-e armv8_pmuv3_0/l1i_tlb/ -e armv8_pmuv3_0/l1i_tlb_refill/ " +
##                     "-e armv8_pmuv3_0/l2d_cache/ 
                     "-e armv8_pmuv3_0/l2d_cache_refill/ " +
  ##                   "-e armv8_pmuv3_0/l2d_cache_wb/ -e armv8_pmuv3_0/l2d_tlb/ " +
    ##                 "-e armv8_pmuv3_0/l2d_tlb_refill/ -e armv8_pmuv3_0/l2i_cache/ " +
      ####               "-e armv8_pmuv3_0/l2i_cache_refill/ -e armv8_pmuv3_0/l2i_tlb/ " +
          ##           "-e armv8_pmuv3_0/l2i_tlb_refill/ -e armv8_pmuv3_0/ll_cache/ " +
             #       "-e armv8_pmuv3_0/ll_cache_miss/
                     "-e armv8_pmuv3_0/ll_cache_miss_rd/ " +
              ##       "-e armv8_pmuv3_0/ll_cache_rd/ " + #-e armv8_pmuv3_0/mem_access/ " +
               #     "-e armv8_pmuv3_0/memory_error/ -e armv8_pmuv3_0/remote_access/ " +
                #    "-e armv8_pmuv3_0/remote_access_rd/ -e armv8_pmuv3_0/sample_collision/ " +
                 #   "-e armv8_pmuv3_0/sample_feed/ -e armv8_pmuv3_0/sample_filtrate/ " +
                  #  "-e armv8_pmuv3_0/sample_pop/ -e armv8_pmuv3_0/stall_backend/ " +
                   # "-e armv8_pmuv3_0/stall_frontend/ -e armv8_pmuv3_0/sw_incr/ " +
                    #"-e armv8_pmuv3_0/ttbr_write_retired/ " +
                    
    
                    #"-e  hisi_sccl7_l3c23/wr_spipe/
#                    "-e exe_stall_cycle -e fetch_bubble " +
 #                   "-e  hit_on_prf -e if_is_stall -e iq_is_empty -e  l1d_cache_inval " +
  #                  "-e  l1d_cache_rd -e  l1d_cache_refill_rd -e  l1d_cache_refill_wr " +
   #                 "-e  l1d_cache_wb_clean -e  l1d_cache_wb_victim -e  l1d_cache_wr " +
    #                "-e  l1d_tlb_rd -e  l1d_tlb_refill_rd -e  l1d_tlb_refill_wr " +
     #               "-e  l1d_tlb_wr -e  l1i_cache_prf -e  l1i_cache_prf_refill " +
##                     "-e  l2d_cache_inval -e  l2d_cache_rd -e  l2d_cache_refill_rd " +
  ##                   "-e  l2d_cache_refill_wr -e  l2d_cache_wb_clean -e  l2d_cache_wb_victim " +
    ##                 "-e  l2d_cache_wr " + #-e  mem_stall_anyload 
      #                 "-e  mem_stall_l1miss " +
      ##               "-e  mem_stall_l2miss " + #-e  prf_req " + # -e uncore_hisi_ddrc.act_cmd " +
#                    "-e uncore_hisi_ddrc.flux_rcmd -e  uncore_hisi_ddrc.flux_wcmd " +
 #                   "-e  uncore_hisi_ddrc.pre_cmd -e  uncore_hisi_ddrc.rnk_chg " +
  #                  "-e  uncore_hisi_ddrc.rw_chg -e  uncore_hisi_hha.rd_ddr_128b " +
   #                 "-e  uncore_hisi_hha.rd_ddr_64b -e  uncore_hisi_hha.rx_ops_num " +
    #                "-e uncore_hisi_hha.rx_outer -e  uncore_hisi_hha.rx_sccl " +
     #               "-e uncore_hisi_hha.wr_ddr_128b -e uncore_hisi_hha.wr_dr_64b " +
        ##             "-e uncore_hisi_l3c.rd_cpipe -e uncore_hisi_l3c.rd_hit_cpipe " +
          ##           "-e uncore_hisi_l3c.victim_num -e uncore_hisi_l3c.wr_cpipe " +
            ##         "-e uncore_hisi_l3c.wr_hit_cpipe " + #-e rNNN " +
       #             " -o " + perf_data_file +
                    " ./" + b_exe_name + " " + subset[1]) # + " -o " + perf_data_file)
            in_name = subset[2]
            split_cmd = shlex.split(cmd)
            spawn_list.append((split_cmd, in_name, tmp_dir, log_filepath))
            execute(spawn_list, args, sem) # execute one by one of subsets, then empty list
            del spawn_list[:]
            #print("subset: " + subset[0])
            if "pass1" in subset[0]: # Copy the ouput from pass1 to input for pass2 in 625 ref
                #print("BR1")
                spec_b_folder = os.path.join(args.spec_dir, b_name)
                b_set = args.set[0]
                #print("b_ser¡t: "+ b_set)
                #print(args.set)
                if not os.path.isdir(os.path.join(spec_b_folder, "data")):
                    rate_b_name = "5" + b_name[1:len(b_name)-1] + "r"
                    spec_b_folder = os.path.join(args.spec_dir, rate_b_name)
                if b_set == "ref":
                    if "_s" in b_name:
                        b_set = ("refspeed" if os.path.isdir(os.path.join(
                            spec_b_folder, "data", "refspeed")) else "refrate")
                    else:
                        b_set = "refrate"
                #print("b_set: " + b_set)
                input_folders_b = [os.path.join(spec_b_folder, "data", b_set, "input"),
                        os.path.join(spec_b_folder, "data", "all", "input")]
                #print("exe: " + b_exe_name)
                #print("input_folders: ")
                #print(input_folders_b)
                for d in input_folders_b:
                    #print("d: "+d)
                    if os.path.isdir(d):
                        os.popen("ls -lht " + tmp_dir)
                        #print("tmp_dir: " + tmp_dir)
                        #print("input: " + d)
                        os.popen("rm -rf " + tmp_dir +"/" + b_exe_name)
                        os.popen("cp -ur " + tmp_dir + "/* " + d + "/")
#    execute(spawn_list, args, sem)
    return


def report(args, sem):
    spawn_list = []
#    check_prerequisites(args, True, False, False, False)

    print("Report data from perf:")
    for b_name in args.benchmarks:
        print("- " + b_name)

        b_spl = b_name.split('.')
        b_abbr = b_spl[0] + b_spl[1]
        b_set = args.set[0]

        # Get benchmark general parameters from benchlist.py
        success, b_params = get_params(args, b_name)

        # Skip this benchmark if some error occurred
        if not success:
            continue

        b_exe_name = b_params[0]
        b_preproc  = b_params[1]

        # Get benchmark subset parameters from benchlist.py
        ss_params = get_ss_params(b_name, b_set)

        for subset in ss_params:
            # Prepare the execution environment
            out_dir, tmp_dir = prepare_env(args, b_name, b_exe_name, b_preproc,
                os.path.join("counter", subset[0]))

            mem_filepath = os.path.join(out_dir, "mem." + b_abbr + "." +
                subset[0])
            log_filepath = os.path.join(out_dir, b_abbr + "." + subset[0] +
                "beta_sampling_perf_extact_instructions_100000000_test22.log")
            perf_data_file = os.path.join(out_dir, b_abbr + "." + subset[0] +
                    "perf_data_sampling_instructions_100000000_test2.data")

            # Execute perf (instead of perf stat, perf record)
            cmd = ("perf report  -i " + perf_data_file + " -t ','")
            in_name = subset[2]
            split_cmd = shlex.split(cmd)
            spawn_list.append((split_cmd, in_name, tmp_dir, log_filepath))

    execute(spawn_list, args, sem)
    return



def main():
    global count_pids
    global count_fail

    try:
        benchlist.benchmarks
        benchlist.exe_name
        benchlist.preprocessing
        benchlist.mem_size
        benchlist.subset
        benchlist.params
        benchlist.input
    except (NameError, AttributeError):
        print("error: unable to load parameters from benchlist.py")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Helper for SPEC simulation")
    parser.add_argument("set", nargs=1, type=str,
        choices=["test","train","ref"], help="simulation set")
    parser.add_argument("benchmarks", nargs="+", type=str,
        help="list of target benchmarks")
    parser.add_argument("-b", "--bbv", action="store_true",
        help="generate basic block vectors")
    parser.add_argument("-s", "--simpoints", action="store_true",
        help="generate simulation points")
    parser.add_argument("-c", "--checkpoints", action="store_true",
        help="generate checkpoints with gem5")
    parser.add_argument("-x", "--execute", action="store_true",
        help="simulate target benchmarks from checkpoints")
    parser.add_argument("-f", "--full", action="store_true",
        help="simulate target benchmarks normally")
    parser.add_argument("-p", "--profile", action="store_true",
        help="profile benchmarks memory utilization with valgrind and massif")
    parser.add_argument("-k", "--counters", action="store_true",
        help="Run benchmark natively registering statistics"+
            " from hardware counters")
    parser.add_argument("-r", "--report", action="store_true",
        help="Extract data from perf record")
    parser.add_argument("--arch", action="store", type=str, default="aarch64",
        choices=["aarch64","armhf","x86-64"], help="cpu architecture " +
        "(default: %(default)s)")
    parser.add_argument("--maxk", action="store", type=int, metavar="N",
        default=30, help="maxK parameter for simpoint (default: %(default)s)")
    parser.add_argument("--int-size", action="store", type=int, metavar="N",
        default=100000000, help="bbv interval size (default: %(default)s)")
    parser.add_argument("--warmup", action="store", type=int, metavar="N",
        default=0, help="number of warmup instructions (default: %(default)s)")
    parser.add_argument("--l2-banks", action="store", type=int, metavar="N",
        default=4, help="number of banks in L2 cache (default: %(default)s)")
    parser.add_argument("--l3-banks", action="store", type=int, metavar="N",
        default=4, help="number of banks in L3 cache (default: %(default)s)")
    parser.add_argument("--l1i-hwp", action="store", type=str, default=None,
        choices=list(simparams.hwp_config), help="L1I prefetcher parameters" +
        " (default: %(default)s)")
    parser.add_argument("--l1d-hwp", action="store", type=str, default=None,
        choices=list(simparams.hwp_config), help="L1D prefetcher parameters" +
        " (default: %(default)s)")
    parser.add_argument("--l2-hwp", action="store", type=str, default=None,
        choices=list(simparams.hwp_config), help="L2 prefetcher parameters" +
        " (default: %(default)s)")
    parser.add_argument("--l3-hwp", action="store", type=str, default=None,
        choices=list(simparams.hwp_config), help="L3 prefetcher parameters" +
        " (default: %(default)s)")
    parser.add_argument("--max-proc", action="store", type=int, metavar="N",
        default=int(os.sysconf('SC_NPROCESSORS_ONLN')),
        help="number of processes that can run concurrently " +
        "(default: %(default)s)")
    parser.add_argument("--mm-sim", nargs=1, type=str, default="none",
        choices=["none","nvmain","ramulator"], help="main memory simulator " +
        "(default: %(default)s)")
    parser.add_argument("--sp-dir", action="store", type=str, metavar="DIR",
        default=(home + "/simpoint"), help="path to simpoint utility " +
        "(default: %(default)s)")
    parser.add_argument("--gem5-dir", action="store", type=str, metavar="DIR",
        default=(home + "/gem5-artecs"), help="path to gem5 simulator " +
        "(default: %(default)s)")
    parser.add_argument("--nvmain-cfg", action="store", type=str,
        metavar="FILE",
        default=(os.getcwd() + "/LPDDR3_micron_512Meg_x32_qdp.config"),
        help="path to NVMAIN configuration file (default: %(default)s)")
    parser.add_argument("--spec-dir", action="store", type=str, metavar="DIR",
        default=(home + "/cpu" + bsyear + "/benchspec/CPU" + (bsyear if
        benchsuite != "spec2017" else "")),
        help="path to SPEC benchmark suite (default: %(default)s)")
    parser.add_argument("--data-dir", action="store", type=str, metavar="DIR",
        default=(home + "/benchmark-data/SPECCPU/speccpu" + bsyear),
        help="path to benchmark simulation data (default: %(default)s)")
    parser.add_argument("--out-dir", action="store", type=str, metavar="DIR",
        default=(home + "/out_" + benchsuite), help="output directory " +
        "(default: %(default)s)")
    parser.add_argument("--cpts", action="store", type=int, metavar="N",
        default=0, help="execute N checkpoints only, in order of weight " +
        "(default: 0 = all)")
    parser.add_argument("--sss", action="store_true",
        help="use a single subset for each benchmark (the first one)")
    parser.add_argument("--mp", action="store_true",
        help="multiprocess environment (one benchmark per core)")
    parser.add_argument("--keep-tmp", action="store_true",
        help="do not remove temporary folders after the execution")
    parser.add_argument("--use-gem5", action="store_true",
        help="use gem5 for bbv generation")
    parser.add_argument("--debug", action="store_true",
        help="use gem5.opt instead of gem5.fast")
    parser.add_argument("--ctrace", action="store_true",
        help="dump conflict trace (implies --debug)")
    parser.add_argument("--atrace", action="store_true",
        help="dump access trace (implies --debug)")
    parser.add_argument("--rename", action="store_true",
        help="rename output files with an unique configuration id")
    parser.add_argument("--no-wd", action="store_true",
        help="disable watchdog")
    args = parser.parse_args()
    if args.ctrace or args.atrace:
        args.debug = True
    if (len(args.benchmarks) == 1 and
        args.benchmarks[0] in benchlist.bench_groups):
        args.benchmarks = list(benchlist.bench_groups[args.benchmarks[0]])
    sem = threading.Semaphore(args.max_proc)

    # Create the operation list
    ops = []
    ops.append(args.bbv)
    ops.append(args.simpoints)
    ops.append(args.checkpoints)
    ops.append(args.execute)
    ops.append(args.full)
    ops.append(args.profile)
    ops.append(args.counters)
    ops.append(args.report)

    # Check if any operation has been selected
    if not True in ops:
        parser.error("no operation selected")
    # Check if ops contains non-consecutive simpoint operations
    elif ((ops[1] == True and ops[2] == False and ops[3] == True) or
        (ops[0] == True and ops[1] == False and ops[2] == True) or
        (ops[0] == True and ops[1] == False and ops[3] == True)):
        parser.error("simpoint-related operations are not consecutive")

    # Check if specified benchmarks actually exist
    for i, b_name in enumerate(args.benchmarks):
        b_found = False
        for bl_bench in benchlist.benchmarks:
            if (b_name == bl_bench or
                b_name == bl_bench.split('.')[0]):
                args.benchmarks[i] = bl_bench
                b_found = True
                break
        if b_found == False:
            print("error: unknown benchmark " + b_name)
            exit(1)

    for i in range(len(ops)):
        if ops[i] == True:
            if i == 0:
                bbv_gen(args, sem)
            elif i == 1:
                sp_gen(args, sem)
            elif i == 2:
                cp_gen(args, sem)
            elif i == 3:
                cp_sim(args, sem)
            elif i == 4:
                full_sim(args, sem)
            elif i == 5:
                profile(args, sem)
            elif i == 6:
                counters(args, sem)
            elif i == 7:
                report(args, sem)

            # Print some statistics
            print("OK!\n")
            print("Number of spawned processes\t= " + str(count_pids))
            print("Number of failed processes\t= " + str(count_fail))
            if count_pids != 0:
                print("Success rate\t\t\t= " +
                    str((1 - float(count_fail) / count_pids) * 100) + "%")
            # Reset the counters for next phase
            count_pids = 0
            count_fail = 0

            # Next operation must fetch data from generated output
            args.data_dir = args.out_dir
            # Add a new line
            print("")


if __name__ == "__main__":
    main()
