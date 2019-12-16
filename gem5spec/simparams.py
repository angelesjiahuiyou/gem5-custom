# CPU MODELS
# ----------

cpu_models = {
    "aarch64" : {
        "HPI"           : "se.py",
        "CortexA15"     : "se.py"   # TODO: figure out whether this is still ok
    },
    "armhf" : {
        "CortexA7"      : "se.py",
        "CortexA15"     : "se.py"
    },
    "x86-64" : {
        "DerivO3CPU"    : "se.py"
    }
}


# MEMORY TECHNOLOGIES
# -------------------
# Tuple: (L1D, L1I, L2)

mem_technologies = {
    #"stt-all"       : ("stt-mram", "stt-mram", "stt-mram"),
    #"stt-l1d"       : ("stt-mram", "sram", "sram"),
    #"stt-l1d-l2"    : ("stt-mram", "sram", "stt-mram"),
    #"stt-l1i"       : ("sram", "stt-mram", "sram"),
    "stt-l2"        : ("sram", "sram", "stt-mram"),
    "stt-none"      : ("sram", "sram", "sram")
}

# MEMORY CASES
# ------------

mem_cases = (
    "typical",
    "worst"
)


# MEMORY CONFIGURATION
# --------------------
# Subtuples:
# - L1I {read, write, tag, resp} latency, size, associativity
# - L1D {read, write, tag, resp} latency, size, associativity
# - L2  {read, write, tag, resp} latency, size, associativity
# --------------------
# Notes: for now SRAM typical = SRAM worst,
#        for now O3CPU latencies = A15 latencies

mem_configs = {
    "DerivO3CPU" : {    # L2 response latency guessed
        "sram" : {
            "typical" : ((2, 2, 2, 2, '32kB', 2), (2, 2, 2, 2, '32kB', 2), (12, 12, 12, 5, '1MB', 8)),
            "worst"   : ((2, 2, 2, 2, '32kB', 2), (2, 2, 2, 2, '32kB', 2), (12, 12, 12, 5, '1MB', 8))
        },
        "stt-mram" : {
            "typical" : ((6,  21, 2, 2, '32kB', 2), (6,  21, 2, 2, '32kB', 2), (12, 21, 12, 5, '1MB', 8)),
            "worst"   : ((12, 40, 2, 2, '32kB', 2), (12, 40, 2, 2, '32kB', 2), (21, 40, 12, 5, '1MB', 8))
        }
    },
    "CortexA7" : {      # L2 response latency guessed
        "sram" : {
            "typical" : ((2, 2, 2, 2, '16kB', 2), (2, 2, 2, 2, '16kB', 4), (8, 8, 8, 8, '256kB', 8)),
            "worst"   : ((2, 2, 2, 2, '16kB', 2), (2, 2, 2, 2, '16kB', 4), (8, 8, 8, 8, '256kB', 8))
        },
        "stt-mram" : {
            "typical" : ((4, 11, 2, 2, '16kB', 2), (4, 11, 2, 2, '16kB', 4), (8,  14, 8, 8, '256kB', 8)),
            "worst"   : ((8, 14, 2, 2, '16kB', 2), (8, 14, 2, 2, '16kB', 4), (14, 28, 8, 8, '256kB', 8))
        }        
    },
    "CortexA15" : {     # L2 response latency guessed
        "sram" : {
            "typical" : ((2, 2, 2, 2, '32kB', 2), (2, 2, 2, 2, '32kB', 2), (12, 12, 12, 5, '1MB', 16)),
            "worst"   : ((2, 2, 2, 2, '32kB', 2), (2, 2, 2, 2, '32kB', 2), (12, 12, 12, 5, '1MB', 16))
        },
        "stt-mram" : {
            "typical" : ((6,  21, 2, 2, '32kB', 2), (6,  21, 2, 2, '32kB', 2), (12, 21, 12, 5, '1MB', 16)),
            "worst"   : ((12, 40, 2, 2, '32kB', 2), (12, 40, 2, 2, '32kB', 2), (21, 40, 12, 5, '1MB', 16))
        }
    },
    "HPI" : {
        "sram" : {      # Use configuration specified in the model
            "typical" : ((1, 1, 1, 1, '32kB', 2), (1, 1, 1, 1, '32kB', 4), (13, 13, 13, 5, '1MB', 16)),
            "worst"   : ((1, 1, 1, 1, '32kB', 2), (1, 1, 1, 1, '32kB', 4), (13, 13, 13, 5, '1MB', 16))
        },
        "stt-mram" : {  # Latencies copied from A15, as sizes are the same
            "typical" : ((6,  21, 1, 1, '32kB', 2), (6,  21, 1, 1, '32kB', 4), (13, 21, 13, 5, '1MB', 16)),
            "worst"   : ((12, 40, 1, 1, '32kB', 2), (12, 40, 1, 1, '32kB', 4), (21, 40, 13, 5, '1MB', 16))
        }        
    }
}