#import pdb
#pdb.set_trace()
# -*- coding: utf-8 -*-

import m5
from m5.objects import *
from caches import *


# Initialize system
system = System()
system.membus = SystemXBar()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '500MHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('2GB')]
system.physmem = SimpleMemory(range=system.mem_ranges[0])
system.physmem.port = system.membus.mem_side_ports

# Set CPU and cache
system.cpu = X86TimingSimpleCPU()

system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()

system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# Configure L2 cache
system.l2bus = L2XBar()
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

system.l2cache = L2Cache() 
system.l2cache.connectCPUSideBus(system.l2bus)
system.l2cache.connectMemSideBus(system.membus)


#system.membus = SystemXBar()

# Set up interrupt controller
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

# Specify the SPEC benchmark executable path
binary = '/home/jiahuiyou/cpu2017/cpu2017/benchspec/CPU/623.xalancbmk_s/exe/xalancbmk_s_base.x86-64'
source_file = '/home/jiahuiyou/cpu2017/cpu2017/data/test.xml'       # XML source file
stylesheet_file = '/home/jiahuiyou/cpu2017/cpu2017/data/stylesheet.xsl'  # XSL stylesheet file

# Create a process for the benchmark
process = Process()
process.cmd = [binary, source_file, stylesheet_file]  # Add the required arguments
system.cpu.workload = process
system.cpu.createThreads()

# Set workload for gem5 version compatibility
system.workload = SEWorkload.init_compatible(binary)

# Instantiate root and run simulation
root = Root(full_system=False, system=system)
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()

if exit_event.getCause() != "no exit event":
    print('Exiting @ tick {} because {}'.format(m5.curTick(), exit_event.getCause()))
else:
    print("Simulation is still running.")


