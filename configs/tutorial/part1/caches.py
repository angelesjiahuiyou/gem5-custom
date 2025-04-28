from m5.objects import Cache, BaseTags, RRIPRP, SetAssociative, BaseSetAssoc

# L1
class L1Cache(Cache):
    assoc = 8
    tag_latency = 2
    data_latency = 3
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
    

# L1 Ins
class L1ICache(L1Cache):
    size = '16kB'
    indexing_policy = SetAssociative(entry_size=16)
    tags_class = BaseTags

    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port

    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports

# L1 Data
class L1DCache(L1Cache):
    size = '64kB'
    indexing_policy = SetAssociative(entry_size=64)
    tags_class = BaseTags

    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port

    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports

# L2 
class L2Cache(Cache):
    size = '1MB'  
    assoc = 32     
    tag_latency = 2
    data_latency = 10
    response_latency = 10
    mshrs = 20
    tgts_per_mshr = 12
    replacement_policy = RRIPRP()  
    indexing_policy = SetAssociative(entry_size=64)
    tags_class = BaseTags  

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports
    
    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports
