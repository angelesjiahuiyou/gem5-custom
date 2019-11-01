# CPU MODELS
# ----------

cpu_models = {
    "arm" : {
        "CortexA7"      : "se_multi.py",
        "CortexA15"     : "se_multi.py"
    },
    "x86" : {
        "DerivO3CPU"    : "se_multi.py"
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


# MEMORY LATENCIES
# ----------------
# Subtuples:
# - L1 {read, write, tag, resp} latency,
# - L2 {read, write, tag, resp} latency.
# ----------------
# Notes: for now SRAM typical = SRAM worst,
#        for now O3CPU latencies = A15 latencies

mem_latencies = {
    "DerivO3CPU" : {
        "sram" : {
            "typical" : ((2,  2,  2, 2), (12, 12, 12, 2)),
            "worst"   : ((2,  2,  2, 2), (12, 12, 12, 2))
        },
        "stt-mram" : {
            "typical" : ((6,  21, 2, 2), (12, 21, 12, 2)),
            "worst"   : ((12, 40, 2, 2), (21, 40, 12, 2))
        }
    },
    "CortexA7" : {
        "sram" : {
            "typical" : ((2, 2,  2, 2), (8,  8,  8, 2)),
            "worst"   : ((2, 2,  2, 2), (8,  8,  8, 2))
        },
        "stt-mram" : {
            "typical" : ((4, 11, 2, 2), (8,  14, 8, 2)),
            "worst"   : ((8, 14, 2, 2), (14, 28, 8, 2))
        }        
    },
    "CortexA15" : {
        "sram" : {
            "typical" : ((2,  2,  2, 2), (12, 12, 12, 2)),
            "worst"   : ((2,  2,  2, 2), (12, 12, 12, 2))
        },
        "stt-mram" : {
            "typical" : ((6,  21, 2, 2), (12, 21, 12, 2)),
            "worst"   : ((12, 40, 2, 2), (21, 40, 12, 2))
        }
    }
}