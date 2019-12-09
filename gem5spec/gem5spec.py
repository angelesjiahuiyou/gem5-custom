# Select the benchmark suite to use
# (allowed values: spec2006, spec2017)
benchsuite = "spec2017"

import argparse
import os
import platform
import subprocess
import sys
import time
import threading

# Local modules
import simparams
dfl_ram = "512MB"
try:
    if benchsuite == "spec2006":
        import benchsuites.spec2006 as benchlist
    elif benchsuite == "spec2017":
        import benchsuites.spec2017 as benchlist
        dfl_ram = "2GB"
    else:
        raise ImportError("Invalid benchmark suite") 
except ImportError as error:
    print(error)
    exit(1)

uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])
home = os.path.expanduser("~")
bsyear = ''.join(c for c in benchsuite if c.isdigit())

# List of all the spawned subprocesses
sp_pids = []
# List of all the failed subprocesses
sp_fail = []
# Shutdown flag
shutdown = False

def cmd_exists(cmd):
    return any(
        os.access(os.path.join(path, cmd), os.X_OK) 
        for path in os.environ["PATH"].split(os.pathsep)
    )


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
    b_mem_size = benchlist.mem_size.get(b_name, "")
    arguments = (b_exe_name, b_preproc, b_mem_size)
    return True, arguments


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


# Remove directories prepared with mirror_dir
def remove_dir(target):
    for root, dirs, files in os.walk(target, topdown=False):
        for name in files:
            os.unlink(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(target)
    return


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
        remove_dir(tmp_dir)

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


# Watchdog which prevents host system memory saturation
def watchdog():
    global sp_pids
    global sp_fail

    total, avail = get_host_mem()
    if float(avail) / float(total) < 0.1 and any(sp_pids):
        # Find the child which is using more memory
        largest_mem = [0, 0]
        for pid in sp_pids:
            mem = get_rss(pid)
            if mem > largest_mem[1]:
                largest_mem[0] = pid
                largest_mem[1] = mem
        # Take note and kill it
        sp_fail.append(largest_mem[0])
        print("watchdog: killing process " + str(largest_mem[0]))
        os.kill(largest_mem[0], 9)
        # Wait some more time
        time.sleep(4)
    return


# Spawn all the programs in the spawn list and control the execution
def execute(spawn_list, sem, keep_tmp):
    global shutdown

    # Create a thread for each child, to release the semaphore after execution
    # (this is needed because with subprocess it is only possible to wait for
    # a specific child to terminate, but we want to perform the operation when
    # ANY of them terminates, regardless of which one does)
    def run_in_thread(s):
        global sp_pids
        global sp_fail

        if not shutdown:
            cmd, dir, logpath = s
            logfile = open(logpath, "w")
            proc = subprocess.Popen(cmd, cwd=dir, stdout=logfile,
                stderr=subprocess.STDOUT)
            pid = proc.pid
            sp_pids.append(pid)
            # Necessary: sometimes the thread is idling inside the routine
            if shutdown and os.path.exists(os.path.join("/proc", str(pid))):
                os.kill(pid, 9)
            proc.wait()

            # Close the log file (after flushing internal buffers)
            logfile.flush()
            os.fsync(logfile.fileno())
            logfile.close()

            # Directories cleanup
            wd_name = dir.split("/")[-1]
            if pid in sp_fail:
                # Purge directory in case of process out of memory
                dir_to_rm = dir if wd_name != "tmp" else uppath(dir, 1)
                remove_dir(dir_to_rm)
            elif not keep_tmp:
                if wd_name == "tmp":
                    remove_dir(dir)

            # Clear entries in sp_fail and sp_pids
            if pid in sp_fail:
                sp_fail.remove(pid)
            if pid in sp_pids:
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
        while(spawn_thread.isAlive()):
            watchdog()
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
        # Check if valgrind exists in current system
        if not cmd_exists("valgrind"):
            print("error: valgrind utility not found in env path")
            exit(2)

        # Check if the CPU architecture matches the execution platform
        machine = platform.machine()
        archs_amd64 = ("x86_64", "x64", "amd64")
        archs_arm = ("arm", "armv7b", "armv7l", "armhf")
        archs_arm64 = ("aarch64_be", "aarch64", "armv8b", "armv8l", "arm64")         
        if ((args.arch == "amd64" and machine not in archs_amd64) or
            (args.arch == "arm" and machine not in archs_arm) or
            (args.arch == "arm64" and machine not in archs_arm64)):
            print("error: architecture mismatch")
            exit(3)
    else:
        # Check if gem5 exists in specified path
        gem5_build = "X86" if args.arch == "amd64" else "ARM"
        gem5_exe_dir  = os.path.join(args.gem5_dir, "build", gem5_build)
        gem5_exe_name = "gem5.opt" if args.debug else "gem5.fast"
        gem5_exe_path = os.path.join(gem5_exe_dir, gem5_exe_name)
        if not os.path.isfile(gem5_exe_path):
            print("error: gem5.fast executable not found in " + gem5_exe_dir)
            exit(2)

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

        # Execute valgrind exp-bbv tool
        for subset in ss_params:

            # Prepare the execution environment
            out_dir, tmp_dir = prepare_env(args, b_name, b_exe_name, b_preproc,
                os.path.join("valgrind", subset[0]))

            bbv_filepath = os.path.join(out_dir, "bb.out." + b_abbr + "." +
                subset[0])
            pc_filepath = os.path.join(out_dir, "pc." + b_abbr + "." +
                subset[0])
            out_filepath = os.path.join(out_dir, b_abbr + "." + subset[0] +
                ".out")
            log_filepath = os.path.join(out_dir, b_abbr + "." + subset[0] +
                ".log")

            if not args.use_gem5:
                # Execute valgrind with exp-bbv tool
                cmd = ("valgrind --tool=exp-bbv --bb-out-file=" +
                    bbv_filepath + " --pc-out-file=" + pc_filepath + " ./" +
                    b_exe_name + " " + subset[1] + (" < " + subset[2] if
                    subset[2] else ""))
            else:
                cmd = (gem5_exe_path + " --outdir=" + out_dir +
                    " " + os.path.join(args.gem5_dir, "configs", "example", 
                    "se.py") + " --cpu-type=NonCachingSimpleCPU" +
                    " --simpoint-profile --simpoint-interval=" +
                    str(args.int_size) + " --output=" + out_filepath +
                    " --mem-size=" + (b_mem_size if b_mem_size else dfl_ram) +
                    " --cmd=./" + b_exe_name +
                    (" --options=\"" + subset[1] + "\"" if subset[1] else "") +
                    (" --input=" + subset[2] if subset[2] else "")).split()
            spawn_list.append((cmd, tmp_dir, log_filepath))

    execute(spawn_list, sem, args.keep_tmp)
    print("done")
    return


def sp_gen(args, sem):
    spawn_list = []

    # Check if simpoint tool exists in specified path
    simpoint_exe = os.path.join(args.sp_dir, "bin", "simpoint")
    if not os.path.isfile(simpoint_exe):
        print("error: simpoint executable not found in " + args.sp_dir)
        exit(2)

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
            data_dir = os.path.join(args.data_dir, base_subfolder, "valgrind",
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
                " -saveSimpointWeights " + wgt_filepath).split()
            spawn_list.append((cmd, out_dir, log_filepath))

    execute(spawn_list, sem, args.keep_tmp)
    print("done")
    return


def cp_gen(args, sem):
    spawn_list = []

    # Check if gem5 exists in specified path
    gem5_build = "X86" if args.arch == "amd64" else "ARM"
    gem5_exe_dir  = os.path.join(args.gem5_dir, "build", gem5_build)
    gem5_exe_name = "gem5.opt" if args.debug else "gem5.fast"
    gem5_exe_path = os.path.join(gem5_exe_dir, gem5_exe_name)
    if not os.path.isfile(gem5_exe_path):
        print("error: gem5.fast executable not found in " + gem5_exe_dir)
        exit(2)

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
                " --mem-size=" + (b_mem_size if b_mem_size else dfl_ram) +
                " --cmd=./" + b_exe_name + (" --options=\"" + subset[1] + "\""
                if subset[1] else "") + (" --input=" + subset[2] if subset[2]
                else "")).split()
            spawn_list.append((cmd, tmp_dir, log_filepath))

    execute(spawn_list, sem, args.keep_tmp)
    print("done")
    return


def cp_sim(args, sem):
    spawn_list = []

    # Check if gem5 exists in specified path
    gem5_build = "X86" if args.arch == "amd64" else "ARM"
    gem5_exe_dir  = os.path.join(args.gem5_dir, "build", gem5_build)
    gem5_exe_name = "gem5.opt" if args.debug else "gem5.fast"
    gem5_exe_path = os.path.join(gem5_exe_dir, gem5_exe_name)
    if not os.path.isfile(gem5_exe_path):
        print("error: gem5.fast executable not found in " + gem5_exe_dir)
        exit(2)

    # Check if specified NVMAIN configuration file exists
    if args.mm_sim == "nvmain" and not os.path.isfile(args.nvmain_cfg):
        print("error: file " + args.nvmain_cfg + " not found")
        exit(2)

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
            cpt_folders = [d for d in sorted(os.listdir(data_ss_dir))
                if cpt_prefix in d]
            if (not any(cpt_folders)):
                print("warning: no checkpoints found in " + data_ss_dir)
                continue

            # Select CPU architecture and corresponding configuration file
            cpu = []
            for model in simparams.cpu_models[args.arch]:
                cpu.append((model, simparams.cpu_models[args.arch][model]))

            # Simulate all possible cases (a lot!)
            instances = [(model, tech, case, cpt) for model in cpu
                for tech in simparams.mem_technologies
                for case in simparams.mem_cases
                for cpt in cpt_folders]
            for i in instances:
                model = i[0]
                tech  = i[1]
                case  = i[2]
                cpt   = i[3]

                model_name = model[0]
                model_conf = model[1]
                hier  = simparams.mem_technologies[tech]

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
                cmd = (gem5_exe_path + " --outdir=" + out_dir +
                    " " + os.path.join(args.gem5_dir, "configs", "example", 
                    model_conf) + " --caches --l2cache" +
                    (" --l2-enable-banks --l2-num-banks=" + str(args.num_banks)
                        if args.num_banks else "") +
                    " --l1d-data-lat=" +  str(cache[hier[0]][case][0][0]) +
                    " --l1d-write-lat=" + str(cache[hier[0]][case][0][1]) +
                    " --l1d-tag-lat=" +   str(cache[hier[0]][case][0][2]) +
                    " --l1d-resp-lat=" +  str(cache[hier[0]][case][0][3]) +
                    " --l1d_size=" +      str(cache[hier[0]][case][0][4]) +
                    " --l1d_assoc=" +     str(cache[hier[0]][case][0][5]) +
                    " --l1i-data-lat=" +  str(cache[hier[1]][case][1][0]) +
                    " --l1i-write-lat=" + str(cache[hier[1]][case][1][1]) +
                    " --l1i-tag-lat=" +   str(cache[hier[1]][case][1][2]) +
                    " --l1i-resp-lat=" +  str(cache[hier[1]][case][1][3]) +
                    " --l1i_size=" +      str(cache[hier[1]][case][1][4]) +
                    " --l1i_assoc=" +     str(cache[hier[1]][case][1][5]) +
                    " --l2-data-lat=" +   str(cache[hier[2]][case][2][0]) +
                    " --l2-write-lat=" +  str(cache[hier[2]][case][2][1]) +
                    " --l2-tag-lat=" +    str(cache[hier[2]][case][2][2]) +
                    " --l2-resp-lat=" +   str(cache[hier[2]][case][2][3]) +
                    " --l2_size=" +       str(cache[hier[2]][case][2][4]) +
                    " --l2_assoc=" +      str(cache[hier[2]][case][2][5]) +
                    " --num-cpus=1" +
                    " --cpu-type=" + model_name +
                    " --restore-simpoint-checkpoint"
                    " --checkpoint-dir=" + data_ss_dir +
                    " --checkpoint-restore=" + str(cpt_folders.index(cpt)+1) +
                    " --output=" + out_filepath +
                    " --mem-size=" + (b_mem_size if b_mem_size else dfl_ram) +
                    " --cmd=./" + b_exe_name +
                    (" --options=\"" + subset[1] + "\"" if subset[1] else "") +
                    (" --input=" + subset[2] if subset[2] else "") +
                    " --mem-type=" + ("NVMainMemory" +
                    " --nvmain-config=" + args.nvmain_cfg +
                    " --nvmain-StatsFile=" + nstats_filepath +
                    " --nvmain-ConfigLog=" + nconf_filepath
                    if args.mm_sim == "nvmain" else "LPDDR3_1600_1x32")
                    ).split()
                spawn_list.append((cmd, tmp_dir, log_filepath))

    execute(spawn_list, sem, args.keep_tmp)
    print("done")
    return


def full_sim(args, sem):
    spawn_list = []

    # Check if gem5 exists in specified path
    gem5_build = "X86" if args.arch == "amd64" else "ARM"
    gem5_exe_dir  = os.path.join(args.gem5_dir, "build", gem5_build)
    gem5_exe_name = "gem5.opt" if args.debug else "gem5.fast"
    gem5_exe_path = os.path.join(gem5_exe_dir, gem5_exe_name)
    if not os.path.isfile(gem5_exe_path):
        print("error: gem5.fast executable not found in " + gem5_exe_dir)
        exit(2)

    # Check if specified NVMAIN configuration file exists
    if args.mm_sim == "nvmain" and not os.path.isfile(args.nvmain_cfg):
        print("error: file " + args.nvmain_cfg + " not found")
        exit(2)

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

            # Select CPU architecture and corresponding configuration file
            cpu = []
            for model in simparams.cpu_models[args.arch]:
                cpu.append((model, simparams.cpu_models[args.arch][model]))

            # Simulate all possible cases
            instances = [(model, tech, case) for model in cpu
                for tech in simparams.mem_technologies
                for case in simparams.mem_cases]
            for i in instances:
                model = i[0]
                tech  = i[1]
                case  = i[2]

                model_name = model[0]
                model_conf = model[1]
                hier  = simparams.mem_technologies[tech]

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
                cmd = (gem5_exe_path + " --outdir=" + out_dir +
                    " " + os.path.join(args.gem5_dir, "configs", "example", 
                    model_conf) + " --caches --l2cache" +
                    (" --l2-enable-banks --l2-num-banks=" + str(args.num_banks)
                        if args.num_banks else "") +
                    " --l1d-data-lat=" +  str(cache[hier[0]][case][0][0]) +
                    " --l1d-write-lat=" + str(cache[hier[0]][case][0][1]) +
                    " --l1d-tag-lat=" +   str(cache[hier[0]][case][0][2]) +
                    " --l1d-resp-lat=" +  str(cache[hier[0]][case][0][3]) +
                    " --l1d_size=" +      str(cache[hier[0]][case][0][4]) +
                    " --l1d_assoc=" +     str(cache[hier[0]][case][0][5]) +
                    " --l1i-data-lat=" +  str(cache[hier[1]][case][1][0]) +
                    " --l1i-write-lat=" + str(cache[hier[1]][case][1][1]) +
                    " --l1i-tag-lat=" +   str(cache[hier[1]][case][1][2]) +
                    " --l1i-resp-lat=" +  str(cache[hier[1]][case][1][3]) +
                    " --l1i_size=" +      str(cache[hier[1]][case][1][4]) +
                    " --l1i_assoc=" +     str(cache[hier[1]][case][1][5]) +
                    " --l2-data-lat=" +   str(cache[hier[2]][case][2][0]) +
                    " --l2-write-lat=" +  str(cache[hier[2]][case][2][1]) +
                    " --l2-tag-lat=" +    str(cache[hier[2]][case][2][2]) +
                    " --l2-resp-lat=" +   str(cache[hier[2]][case][2][3]) +
                    " --l2_size=" +       str(cache[hier[2]][case][2][4]) +
                    " --l2_assoc=" +      str(cache[hier[2]][case][2][5]) +
                    " --num-cpus=1" +
                    " --cpu-type=" + model_name +
                    " --output=" + out_filepath +
                    " --mem-size=" + (b_mem_size if b_mem_size else dfl_ram) +
                    " --cmd=./" + b_exe_name +
                    (" --options=\"" + subset[1] + "\"" if subset[1] else "") +
                    (" --input=" + subset[2] if subset[2] else "") +
                    " --mem-type=" + ("NVMainMemory" +
                    " --nvmain-config=" + args.nvmain_cfg +
                    " --nvmain-StatsFile=" + nstats_filepath +
                    " --nvmain-ConfigLog=" + nconf_filepath
                    if args.mm_sim == "nvmain" else "LPDDR3_1600_1x32")
                    ).split()
                spawn_list.append((cmd, tmp_dir, log_filepath))

    execute(spawn_list, sem, args.keep_tmp)
    print("done")
    return


def main():
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
    parser.add_argument("--arch", action="store", type=str, default="arm",
        choices=["amd64","arm","arm64"], help="cpu architecture " +
        "(default: %(default)s)")
    parser.add_argument("--maxk", action="store", type=int, metavar="N",
        default=30, help="maxK parameter for simpoint (default: %(default)s)")
    parser.add_argument("--int-size", action="store", type=int, metavar="N",
        default=100000000, help="bbv interval size (default: %(default)s)")
    parser.add_argument("--warmup", action="store", type=int, metavar="N",
        default=0, help="number of warmup instructions (default: %(default)s)")
    parser.add_argument("--num-banks", action="store", type=int, metavar="N",
        default=8, help="number of banks in L2 cache (default: %(default)s)")
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
    parser.add_argument("--keep-tmp", action="store_true",
        help="do not remove temporary folders after the execution")
    parser.add_argument("--use-gem5", action="store_true",
        help="use gem5 for bbv generation")
    parser.add_argument("--debug", action="store_true",
        help="use gem5.opt instead of gem5.fast")
    args = parser.parse_args()
    sem  = threading.Semaphore(args.max_proc)

    # Create the operation list
    ops = []
    ops.append(args.bbv)
    ops.append(args.simpoints)
    ops.append(args.checkpoints)
    ops.append(args.execute)
    ops.append(args.full)

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

            # Next operation must fetch data from generated output
            args.data_dir = args.out_dir
            # Add a new line
            print("")


if __name__ == "__main__":
    main()
