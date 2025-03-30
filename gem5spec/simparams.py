# CPU MODELS
# ----------
# Tuple: (core type, configuration file, voltage, frequency)
cpu_models = {
    "aarch64" : {
        "taishan"   : ("DerivO3CPU", "se.py", "0.9V", "2.6GHz")
        #"sc-a53-odn2"   : ("HPI", "se.py", "0.82V", "1.536GHz"),
       # "sc-imec-a15"   : ("CortexA15", "se.py", "1.32V", "2.1GHz")   # TODO: figure out whether this is still ok
    },
    "armhf" : {
        "sc-imec-a7"    : ("CortexA7",  "se.py", "1.27V", "1.4GHz"),
        "sc-imec-a15"   : ("CortexA15", "se.py", "1.32V", "2.1GHz")
    },
    "x86-64" : {
        "sc-i7-6700"    : ("DerivO3CPU", "se.py", "1.32V", "4.0GHz") 
    }
}
# Voltages:
# https://www.researchgate.net/publication/316490969_Experiments_with_Odroid-XU3_board
# https://www.anandtech.com/show/9878/the-huawei-mate-8-review/3


# MEMORY TECHNOLOGIES
# -------------------
# Tuple: (L1D, L1I, L2)
mem_technologies = {
    "default": {
        "sram-only"     : ("sram", "sram", "sram", "sram")
        #"stt-l2"        : ("sram", "sram", "stt-mram", "none"),
        #"sram-only"     : ("sram", "sram", "sram", "none")
    },
    "sc-i7-6700": {
        "stt-l3"        : ("sram", "sram", "sram", "stt-mram"),
        "sram-only"     : ("sram", "sram", "sram", "sram")
    }
}


# MEMORY CASES
# ------------
mem_cases = {
    "default": {
        "typical"#,
        #"w-write",
       # "worst"
    },
    "sram-only": {
        "typical"
    }
}

# PREFETCHER PARAMETERS
# ---------------------
# Tuple: (type, degree, latency, queue size)
hwp_config = {
    "stride1"   : ("StridePrefetcher", 1, 1, 0),
    "stride4q"  : ("StridePrefetcher", 4, 0, 4),
    "stride8"   : ("StridePrefetcher", 8, 1, 0)
}

# MEMORY CONFIGURATION
# --------------------
# Subtuples:
# - L1I {read, write, tag, resp} latency, size, associativity
# - L1D {read, write, tag, resp} latency, size, associativity
# - L2  {read, write, tag, resp} latency, size, associativity
# - L3  {read, write, tag, resp} latency, size, associativity (optional)
# --------------------
# Notes: for now SRAM typical = SRAM worst,
#        for now O3CPU latencies = A15 latencies
mem_configs = {
    "taishan" : {    # L3 response latency guessed, L3 size is the average per-core (2MB x 4 = 8MB total) TODO taishan
        "sram" : {
            "typical"   : ((4, 4, 2, 2, '64kB', 4), (4, 4, 2, 2, '64kB', 4), (8, 8, 2, 2, '512kB', 8), (37, 37, 37, 27, '1MB', 16))#,
            #"w-write"   : ((4, 4, 4, 4, '32kB', 8), (4, 4, 4, 4, '32kB', 8), (8, 8, 8, 8, '256kB', 4), (30, 30, 30, 20, '2MB', 16)),
            #"worst"     : ((4, 4, 4, 4, '32kB', 8), (4, 4, 4, 4, '32kB', 8), (8, 8, 8, 8, '256kB', 4), (30, 30, 30, 20, '2MB', 16))
        }
    },
    "sc-i7-6700" : {    # L3 response latency guessed, L3 size is the average per-core (2MB x 4 = 8MB total)
        "sram" : {
            "typical"   : ((4, 4, 4, 4, '32kB', 8), (4, 4, 4, 4, '32kB', 8), (8, 8, 8, 8, '256kB', 4), (30, 30, 30, 20, '2MB', 16)),
            "w-write"   : ((4, 4, 4, 4, '32kB', 8), (4, 4, 4, 4, '32kB', 8), (8, 8, 8, 8, '256kB', 4), (30, 30, 30, 20, '2MB', 16)),
            "worst"     : ((4, 4, 4, 4, '32kB', 8), (4, 4, 4, 4, '32kB', 8), (8, 8, 8, 8, '256kB', 4), (30, 30, 30, 20, '2MB', 16))
        },
        "stt-mram" : {  # TODO: check L2
            "typical"   : ((12, 40, 4, 4, '32kB', 8), (12, 40, 4, 4, '32kB', 8), (23, 40, 8, 8, '256kB', 4), (31, 55,  30, 20, '2MB', 16)),
            "w-write"   : ((12, 77, 4, 4, '32kB', 8), (12, 77, 4, 4, '32kB', 8), (23, 80, 8, 8, '256kB', 4), (31, 107, 30, 20, '2MB', 16)),
            "worst"     : ((23, 77, 4, 4, '32kB', 8), (23, 77, 4, 4, '32kB', 8), (40, 80, 8, 8, '256kB', 4), (55, 107, 30, 20, '2MB', 16))
        }
    },
    "sc-imec-a7" : {
        "sram" : {
            "typical"   : ((2, 2, 2, 2, '16kB', 2), (2, 2, 2, 2, '16kB', 4), (8, 8, 8, 8, '256kB', 8)),
            "w-write"   : ((2, 2, 2, 2, '16kB', 2), (2, 2, 2, 2, '16kB', 4), (8, 8, 8, 8, '256kB', 8)),
            "worst"     : ((2, 2, 2, 2, '16kB', 2), (2, 2, 2, 2, '16kB', 4), (8, 8, 8, 8, '256kB', 8))
        },
        "stt-mram" : {
            "typical"   : ((4, 11, 2, 2, '16kB', 2), (4, 11, 2, 2, '16kB', 4), (8,  14, 8, 8, '256kB', 8)),
            "w-write"   : ((4, 14, 2, 2, '16kB', 2), (4, 14, 2, 2, '16kB', 4), (8,  28, 8, 8, '256kB', 8)),
            "worst"     : ((8, 14, 2, 2, '16kB', 2), (8, 14, 2, 2, '16kB', 4), (14, 28, 8, 8, '256kB', 8))
        }        
    },
    "sc-imec-a15" : {
        "sram" : {
            "typical"   : ((2, 2, 2, 2, '32kB', 2), (2, 2, 2, 2, '32kB', 2), (12, 12, 12, 12, '1MB', 16)),
            "w-write"   : ((2, 2, 2, 2, '32kB', 2), (2, 2, 2, 2, '32kB', 2), (12, 12, 12, 12, '1MB', 16)),
            "worst"     : ((2, 2, 2, 2, '32kB', 2), (2, 2, 2, 2, '32kB', 2), (12, 12, 12, 12, '1MB', 16))
        },
        "stt-mram" : {
            "typical"   : ((6,  21, 2, 2, '32kB', 2), (6,  21, 2, 2, '32kB', 2), (12, 21, 12, 12, '1MB', 16)),
            "w-write"   : ((6,  40, 2, 2, '32kB', 2), (6,  40, 2, 2, '32kB', 2), (12, 40, 12, 12, '1MB', 16)),
            "worst"     : ((12, 40, 2, 2, '32kB', 2), (12, 40, 2, 2, '32kB', 2), (21, 40, 12, 12, '1MB', 16))
        }
    },
    "sc-a53-odn2" : {
        "sram" : {
            "typical"   : ((4, 4, 4, 4, '32kB', 2), (4, 4, 4, 4, '32kB', 4), (9, 9, 9, 9, '512kB', 16)),
            "w-write"   : ((4, 4, 4, 4, '32kB', 2), (4, 4, 4, 4, '32kB', 4), (9, 9, 9, 9, '512kB', 16)),
            "worst"     : ((4, 4, 4, 4, '32kB', 2), (4, 4, 4, 4, '32kB', 4), (9, 9, 9, 9, '512kB', 16))
        },
        "stt-mram" : {  # Latencies similar to the same config in A15 (sizes are the same)
            "typical"   : ((5, 16, 4, 4, '32kB', 2), (5, 16, 4, 4, '32kB', 4), (9,  16, 9, 9, '512kB', 16)),
            "w-write"   : ((5, 30, 4, 4, '32kB', 2), (5, 30, 4, 4, '32kB', 4), (9,  31, 9, 9, '512kB', 16)),
            "worst"     : ((9, 30, 4, 4, '32kB', 2), (9, 30, 4, 4, '32kB', 4), (16, 31, 9, 9, '512kB', 16))
        }        
    }
}
