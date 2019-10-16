# Select the benchmark suite to use
# (allowed values: spec2006, spec2017)
benchsuite = "spec2017"

import sys
import os
import argparse
import subprocess
import platform
import threading
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

home = os.path.expanduser("~")
bsyear = ''.join(c for c in benchsuite if c.isdigit())

def cmd_exists(cmd):
    return any(
        os.access(os.path.join(path, cmd), os.X_OK) 
        for path in os.environ["PATH"].split(os.pathsep)
    )


def get_params(args, b_name):
    spec_b_folder = args.spec_dir + "/" + b_name
    b_spl = b_name.split('.')

    # Check if the benchmark folder is present in SPEC path
    if not os.path.exists(spec_b_folder):
        print("warning: " + b_name + " not found in " + args.spec_dir)
        return False, (None, None, None)

    # Check if the executable exists
    if b_name in benchlist.exe_name:
        b_exe_name = benchlist.exe_name[b_name] + "_base." + args.arch
    else:
        b_exe_name = b_spl[1] + "_base." + args.arch
    b_exe_folder = args.spec_dir + "/" + b_name + "/exe"
    b_exe_path = b_exe_folder + "/" + b_exe_name
    if not os.path.isfile(b_exe_path):
        print("warning: executable not found in " + b_exe_folder)
        return False, (None, None, None)

    b_preproc  = benchlist.preprocessing.get(b_name, "")
    b_mem_size = benchlist.mem_size.get(b_name, "")
    arguments = (b_exe_path, b_preproc, b_mem_size)
    return True, arguments


def get_ss_params(b_name, b_set):
    benchlist_subset = benchlist.subset.get(b_set)
    benchlist_params = benchlist.params.get(b_set)
    benchlist_input  = benchlist.input.get(b_set)
    if any(v is None for v in
        (benchlist_subset, benchlist_params, benchlist_input)):
        print("error: couldn't find benchmark set")
        exit(3)
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


def prepare_env(args, b_name, b_preproc, target_dir):
    spec_b_folder = args.spec_dir + "/" + b_name
    base_subfolder = "/" + args.arch + "/" + b_name
    out_dir = args.out_dir + base_subfolder + "/" + target_dir
    tmp_dir = out_dir + "/tmp"

    # Create the output folder and the temporary one
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir , mode=0o755)
    for f in os.listdir(tmp_dir):
        os.unlink(tmp_dir + "/" + f)

    # Make a symlink to input data in the temporary directory
    input_folder = [spec_b_folder + "/data/" + args.set[0] + "/input", 
        spec_b_folder + "/data/all/input"]
    for d in input_folder:
        if os.path.exists(d):
            for f in os.listdir(d):
                os.symlink(d + "/" + f, tmp_dir + "/" + f)

    # Do preprocessing of input data if necessary
    arch_bits = 64
    endianness = "le"

    cmd = benchlist.get_preprocessing(b_name, arch_bits, endianness)
    if cmd != None:
        proc = subprocess.Popen(cmd, shell=True, cwd=tmp_dir)
        proc.wait()

    return out_dir, tmp_dir


def spawn(cmd, dir, logpath, sem):
    # Create a thread for each child, to release the semaphore after execution
    # (this is needed because with subprocess it is only possible to wait for
    # a specific child to terminate, but we want to perform the operation when
    # ANY of them terminates, regardless of which one does)
    def run_in_thread(cmd, dir):
        logfile = open(logpath, "w")
        proc = subprocess.Popen(cmd, shell=True, cwd=dir, stdout=logfile,
            stderr=subprocess.STDOUT)
        proc.wait()
        logfile.close()

        # Delete the temporary folder, if present
        subdir = dir.split("/")[-1]
        if subdir == "tmp":
            for f in os.listdir(dir):
                os.unlink(dir + "/" + f)
            os.rmdir(dir)

        # Release the semaphore (makes space for other processes)
        sem.release()
        return

    # Acquire the semaphore (limits the number of active processes)
    sem.acquire()
    thread = threading.Thread(target=run_in_thread, args=(cmd, dir))
    thread.start()
    return thread


def wait_all(threads):
    # Wait for all threads to terminate
    for t in threads:
        t.join()
    return


def bbv_gen(args, sem):
    bbv_threads = []

    # Check if valgrind exists in current system
    if not cmd_exists("valgrind"):
        print("error: valgrind utility not found in env path")
        exit(2)

    # Check if the CPU architecture matches the execution platform
    machine = platform.machine()
    if ((machine in ("i386", "i686", "x86", "x86_64", "x64") and
        args.arch != "x86") or
        (machine in ("arm", "aarch64_be", "aarch64", "armv8b", "armv8l",
            "arm64", "armv7b", "armv7l", "armhf") and args.arch != "arm")):
        print("error: architecture mismatch")
        exit(3)

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

        b_exe_path = b_params[0]
        b_preproc  = b_params[1]

        # Get benchmark subset parameters from benchlist.py
        ss_params = get_ss_params(b_name, b_set) 

        # Execute valgrind exp-bbv tool
        for subset in ss_params:

            # Prepare the execution environment
            out_dir, tmp_dir = prepare_env(args, b_name, b_preproc,
                "valgrind/" + subset[0])

            bbv_filepath = out_dir + "/bb.out." + b_abbr + "." + subset[0]
            pc_filepath = out_dir + "/pc." + b_abbr + "." + subset[0]
            log_filepath = out_dir + "/" + b_abbr + "." + subset[0] + ".out"

            # Execute valgrind with exp-bbv tool
            cmd = ("valgrind --tool=exp-bbv --bb-out-file=" + bbv_filepath +
                " --pc-out-file=" + pc_filepath + " " + b_exe_path +
                " " + subset[1] + (" < " + subset[2] if subset[2] else ""))
            bbv_threads.append(spawn(cmd, tmp_dir, log_filepath, sem))

    wait_all(bbv_threads)
    print("done")
    return


def sp_gen(args, sem):
    sp_threads = []

    # Check if simpoint tool exists in specified path
    simpoint_exec = args.sp_dir + "/bin/simpoint"
    if not os.path.isfile(simpoint_exec):
        print("error: simpoint executable not found in " + args.sp_dir)
        exit(2)

    print("Simpoints generation:")
    for b_name in args.benchmarks:
        print("- " + b_name)

        base_subfolder = "/" + args.arch + "/" + b_name
        b_spl = b_name.split('.')
        b_abbr = b_spl[0] + b_spl[1]
        b_set = args.set[0]

        # Get benchmark subset parameters from benchlist.py
        ss_params = get_ss_params(b_name, b_set)

        for subset in ss_params:
            out_dir = args.out_dir + base_subfolder + "/simpoint/" + subset[0]
            data_dir = (args.data_dir + base_subfolder + "/valgrind/" +
                subset[0])
            bbv_filename = "bb.out." + b_abbr + "." + subset[0]
            bbv_filepath = data_dir + "/" + bbv_filename

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
            if not os.path.exists(out_dir):
                os.makedirs(out_dir, mode=0o755)

            sp_filepath = out_dir + "/simpoint_" + subset[0]
            wgt_filepath = out_dir + "/weight_" + subset[0]
            log_filepath = out_dir + "/log_" + subset[0]

            # Execute the simpoint utility
            cmd = (simpoint_exec + " -loadFVFile " + bbv_filepath + " -maxK " +
                str(args.maxk) + " -saveSimpoints " + sp_filepath +
                " -saveSimpointWeights " + wgt_filepath)
            sp_threads.append(spawn(cmd, out_dir, log_filepath, sem))    

    wait_all(sp_threads)
    print("done")
    return


def cp_gen(args, sem):
    cp_gen_threads = []

    # Check if gem5 exists in specified path
    gem5_exe_dir  = args.gem5_dir + "/build/" + args.arch.upper() 
    gem5_exe_path = gem5_exe_dir + "/gem5.fast"
    if not os.path.isfile(gem5_exe_path):
        print("error: gem5.fast executable not found in " + gem5_exe_dir)
        exit(2)

    print("Checkpoints generation:")
    for b_name in args.benchmarks:
        print("- " + b_name)

        base_subfolder = "/" + args.arch + "/" + b_name
        b_spl = b_name.split('.')
        b_abbr = b_spl[0] + b_spl[1]
        b_set = args.set[0]

        # Get benchmark general parameters from benchlist.py
        success, b_params = get_params(args, b_name)
        
        # Skip this benchmark if some error occurred
        if not success:
            continue

        b_exe_path = b_params[0]
        b_preproc  = b_params[1]
        b_mem_size = b_params[2]

        # Get benchmark subset parameters from benchlist.py
        ss_params = get_ss_params(b_name, b_set) 

        for subset in ss_params:
            data_dir = (args.data_dir + base_subfolder + "/simpoint/" +
                subset[0])
            sp_filename = "simpoint_" + subset[0]
            wgt_filename = "weight_" + subset[0]
            sp_filepath = data_dir + "/" + sp_filename
            wgt_filepath = data_dir + "/" + wgt_filename

            # Check if simpoints are present in the specified data directory
            if (not os.path.isfile(sp_filepath)):
                print("warning: " + sp_filename + " not found in " + data_dir)
                continue
            elif (not os.path.isfile(wgt_filepath)):
                print("warning: " + wgt_filename + " not found in " + data_dir)
                continue

            out_dir, tmp_dir = prepare_env(args, b_name, b_preproc,
                "checkpoint/" + subset[0])

            out_filepath = out_dir + "/" + b_abbr + ".out"
            log_filepath = out_dir + "/gem5." + b_abbr + ".out"

            cmd = ("(time " + gem5_exe_path + " --outdir=" + out_dir + " " +
                args.gem5_dir + "/configs/example/se.py " +
                "--cpu-type=AtomicSimpleCPU --take-simpoint-checkpoint=" +
                sp_filepath + "," + wgt_filepath + "," + str(args.int_size) +
                "," + str(args.warmup) + " --output=" + out_filepath +
                " --mem-size=" + (str(b_mem_size) if b_mem_size else "512MB") +
                " --cmd=" + b_exe_path + (" --options=\"" + subset[1] + "\""
                if subset[1] else "") + (" --input=" + subset[2] if subset[2]
                else "") + ")")
            cp_gen_threads.append(spawn(cmd, tmp_dir, log_filepath, sem))

    wait_all(cp_gen_threads)
    print("done")
    return


def cp_sim(args, sem):
    cp_sim_threads = []

    # Check if gem5 exists in specified path
    gem5_exe_dir  = args.gem5_dir + "/build/" + args.arch.upper() 
    gem5_exe_path = gem5_exe_dir + "/gem5.fast"
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

        base_subfolder = "/" + args.arch + "/" + b_name
        data_dir = args.data_dir + base_subfolder + "/checkpoint"
        b_spl = b_name.split('.')
        b_abbr = b_spl[0] + b_spl[1]
        b_set = args.set[0]

        # Get benchmark general parameters from benchlist.py
        success, b_params = get_params(args, b_name)
        
        # Skip this benchmark if some error occurred
        if not success:
            continue

        b_exe_path = b_params[0]
        b_preproc  = b_params[1]
        b_mem_size = b_params[2]

        # Get benchmark subset parameters from benchlist.py
        ss_params = get_ss_params(b_name, b_set) 

        for subset in ss_params:
            data_ss_dir = data_dir + "/" + subset[0]
            cpt_prefix = "cpt.simpoint_"

            # Check if checkpoints are present in the specified data directory
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

                out_dir, tmp_dir = prepare_env(args, b_name,
                    b_preproc, "simulation/" + subset[0] + "/" + model_name +
                    "/" + tech + "/" + case + "/" + cpt)

                out_filepath = out_dir + "/" + b_abbr + ".out"
                log_filepath = out_dir + "/gem5." + b_abbr + ".out"
                nstats_filepath = out_dir + "/nvmain_stats." + b_abbr + ".log"
                nconf_filepath = out_dir + "/nvmain_config." + b_abbr + ".log"
            
                latencies = simparams.mem_latencies[model_name]
                cmd = ("(time " + gem5_exe_path + " --outdir=" + out_dir +
                    " " + args.gem5_dir + "/configs/example/" + model_conf +
                    " --caches --l2cache" +
                    (" --l2-enable-banks --l2-num-banks=" + str(args.num_banks)
                        if args.num_banks else "") +
                    " --l1d-data-lat=" + str(latencies[hier[0]][case][0][0]) +
                    " --l1d-write-lat=" + str(latencies[hier[0]][case][0][1]) +
                    " --l1d-tag-lat=" + str(latencies[hier[0]][case][0][2]) +
                    " --l1d-resp-lat=" + str(latencies[hier[0]][case][0][3]) +
                    " --l1i-data-lat=" + str(latencies[hier[1]][case][0][0]) +
                    " --l1i-write-lat=" + str(latencies[hier[1]][case][0][1]) +
                    " --l1i-tag-lat=" + str(latencies[hier[1]][case][0][2]) +
                    " --l1i-resp-lat=" + str(latencies[hier[1]][case][0][3]) +
                    " --l2-data-lat=" + str(latencies[hier[2]][case][1][0]) +
                    " --l2-write-lat=" + str(latencies[hier[2]][case][1][1]) +
                    " --l2-tag-lat=" + str(latencies[hier[2]][case][1][2]) +
                    " --l2-resp-lat=" + str(latencies[hier[2]][case][1][3]) +
                    " --num-cpus=1" +
                    " --cpu-type=" + model_name +
                    " --restore-simpoint-checkpoint"
                    " --checkpoint-dir=" + data_ss_dir +
                    " --checkpoint-restore=" + str(cpt_folders.index(cpt)+1) +
                    " --output=" + out_filepath +
                    " --mem-size=" + (str(b_mem_size) if b_mem_size else
                        "512MB") +
                    " --cmd=" + b_exe_path +
                    (" --options=\"" + subset[1] + "\"" if subset[1] else "") +
                    (" --input=" + subset[2] if subset[2] else "") +
                    (" --mem-type=NVMainMemory" +
                    " --nvmain-config=" + args.nvmain_cfg +
                    " --nvmain-StatsFile=" + nstats_filepath +
                    " --nvmain-ConfigLog=" + nconf_filepath
                    if args.mm_sim == "nvmain" else "") +
                    ")")
                cp_sim_threads.append(spawn(cmd, tmp_dir, log_filepath, sem))

    wait_all(cp_sim_threads)
    print("done")
    return


def full_sim(args, sem):
    full_sim_threads = []

    # Check if gem5 exists in specified path
    gem5_exe_dir  = args.gem5_dir + "/build/" + args.arch.upper() 
    gem5_exe_path = gem5_exe_dir + "/gem5.fast"
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

        b_exe_path = b_params[0]
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

                out_dir, tmp_dir = prepare_env(args, b_name,
                    b_preproc, "simulation/" + subset[0] + "/" + model_name +
                    "/" + tech + "/" + case + "/full")

                out_filepath = out_dir + "/" + b_abbr + ".out"
                log_filepath = out_dir + "/gem5." + b_abbr + ".out"
                nstats_filepath = out_dir + "/nvmain_stats." + b_abbr + ".log"
                nconf_filepath = out_dir + "/nvmain_config." + b_abbr + ".log"
            
                latencies = simparams.mem_latencies[model_name]
                cmd = ("(time " + gem5_exe_path + " --outdir=" + out_dir +
                    " " + args.gem5_dir + "/configs/example/" + model_conf +
                    " --caches --l2cache" +
                    (" --l2-enable-banks --l2-num-banks=" + str(args.num_banks)
                        if args.num_banks else "") +
                    " --l1d-data-lat=" + str(latencies[hier[0]][case][0][0]) +
                    " --l1d-write-lat=" + str(latencies[hier[0]][case][0][1]) +
                    " --l1d-tag-lat=" + str(latencies[hier[0]][case][0][2]) +
                    " --l1d-resp-lat=" + str(latencies[hier[0]][case][0][3]) +
                    " --l1i-data-lat=" + str(latencies[hier[1]][case][0][0]) +
                    " --l1i-write-lat=" + str(latencies[hier[1]][case][0][1]) +
                    " --l1i-tag-lat=" + str(latencies[hier[1]][case][0][2]) +
                    " --l1i-resp-lat=" + str(latencies[hier[1]][case][0][3]) +
                    " --l2-data-lat=" + str(latencies[hier[2]][case][1][0]) +
                    " --l2-write-lat=" + str(latencies[hier[2]][case][1][1]) +
                    " --l2-tag-lat=" + str(latencies[hier[2]][case][1][2]) +
                    " --l2-resp-lat=" + str(latencies[hier[2]][case][1][3]) +
                    " --num-cpus=1" +
                    " --cpu-type=" + model_name +
                    " --output=" + out_filepath +
                    " --mem-size=" + (str(b_mem_size) if b_mem_size else
                        "512MB") +
                    " --cmd=" + b_exe_path +
                    (" --options=\"" + subset[1] + "\"" if subset[1] else "") +
                    (" --input=" + subset[2] if subset[2] else "") +
                    (" --mem-type=NVMainMemory" +
                    " --nvmain-config=" + args.nvmain_cfg +
                    " --nvmain-StatsFile=" + nstats_filepath +
                    " --nvmain-ConfigLog=" + nconf_filepath
                    if args.mm_sim == "nvmain" else "") +
                    ")")
                full_sim_threads.append(spawn(cmd, tmp_dir, log_filepath, sem))

    wait_all(full_sim_threads)
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
        help="generate bbv with valgrind")
    parser.add_argument("-s", "--simpoints", action="store_true",
        help="generate simulation points")
    parser.add_argument("-c", "--checkpoints", action="store_true",
        help="generate checkpoints with gem5")
    parser.add_argument("-x", "--execute", action="store_true",
        help="simulate target benchmarks from checkpoints")
    parser.add_argument("-f", "--full", action="store_true",
        help="simulate target benchmarks normally")
    parser.add_argument("--arch", action="store", type=str, default="arm",
        choices=["arm","x86"], help="cpu architecture (default: %(default)s)")
    parser.add_argument("--maxk", action="store", type=int, metavar="N",
        default=30, help="maxK parameter for simpoint (default: %(default)s)")
    parser.add_argument("--int-size", action="store", type=int, metavar="N",
        default=100000000, help="bbv interval size (default: %(default)s)")
    parser.add_argument("--warmup", action="store", type=int, metavar="N",
        default=0, help="number of warmup instructions (default: %(default)s)")
    parser.add_argument("--num-banks", action="store", type=int, metavar="N",
        default=8, help="number of banks in L2 cache (default: %(default)s)")
    parser.add_argument("--max-proc", action="store", type=int, metavar="N",
        default=32, help="number of processes that can run concurrently " +
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
        default=(home + "/benchmarks/SPECCPU/speccpu" + bsyear),
        help="path to benchmark simulation data (default: %(default)s)")
    parser.add_argument("--out-dir", action="store", type=str, metavar="DIR",
        default=(home + "/benchdata_" + benchsuite), help="output directory " +
        "(default: %(default)s)")
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