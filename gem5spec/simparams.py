# CPU MODELS
# ----------

cpu_models = {
    "amd64" : {
        "DerivO3CPU"    : "se_multi.py"
    },
    "arm" : {
        "CortexA7"      : "se_multi.py",
        "CortexA15"     : "se_multi.py"
    },
    "arm64" : {
        "CortexA7"      : "se_multi.py",
        "CortexA15"     : "se_multi.py"
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
    "DerivO3CPU" : {
        "sram" : {
            "typical" : ((2,  2,  2, 2, '32kB', 2), (2,  2,  2, 2, '64kB', 2), (12, 12, 12, 2, '2MB', 8)),
            "worst"   : ((2,  2,  2, 2, '32kB', 2), (2,  2,  2, 2, '64kB', 2), (12, 12, 12, 2, '2MB', 8))
        },
        "stt-mram" : {
            "typical" : ((6,  21, 2, 2, '32kB', 2), (6,  21, 2, 2, '64kB', 2), (12, 21, 12, 2, '2MB', 8)),
            "worst"   : ((12, 40, 2, 2, '32kB', 2), (12, 40, 2, 2, '64kB', 2), (21, 40, 12, 2, '2MB', 8))
        }
    },
    "CortexA7" : {
        "sram" : {
            "typical" : ((2, 2,  2, 2, '16kB', 2), (2, 2,  2, 2, '16kB', 4), (8,  8,  8, 2, '256kB', 8)),
            "worst"   : ((2, 2,  2, 2, '16kB', 2), (2, 2,  2, 2, '16kB', 4), (8,  8,  8, 2, '256kB', 8))
        },
        "stt-mram" : {
            "typical" : ((4, 11, 2, 2, '16kB', 2), (4, 11, 2, 2, '16kB', 4), (8,  14, 8, 2, '256kB', 8)),
            "worst"   : ((8, 14, 2, 2, '16kB', 2), (8, 14, 2, 2, '16kB', 4), (14, 28, 8, 2, '256kB', 8))
        }        
    },
    "CortexA15" : {
        "sram" : {
            "typical" : ((2,  2,  2, 2, '32kB', 2), (2,  2,  2, 2, '32kB', 2), (12, 12, 12, 2, '1MB', 16)),
            "worst"   : ((2,  2,  2, 2, '32kB', 2), (2,  2,  2, 2, '32kB', 2), (12, 12, 12, 2, '1MB', 16))
        },
        "stt-mram" : {
            "typical" : ((6,  21, 2, 2, '32kB', 2), (6,  21, 2, 2, '32kB', 2), (12, 21, 12, 2, '1MB', 16)),
            "worst"   : ((12, 40, 2, 2, '32kB', 2), (12, 40, 2, 2, '32kB', 2), (21, 40, 12, 2, '1MB', 16))
        }
    }
}