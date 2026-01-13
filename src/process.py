class Process:
    """
    Represents a process in the operating system.
    
    Attributes:
        pid (int): Process ID
        arrival_time (int): Time when process arrives in the system
        burst_time (int): Total CPU time required
        memory_required (int): Memory needed in MB
        priority (int): Priority level (lower number = higher priority)
    """
    
    def __init__(self, pid, arrival_time, burst_time, memory_required, priority=0):
        # Basic process attributes
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time  # For preemptive scheduling
        self.memory_required = memory_required
        self.priority = priority
        
        # Timing metrics (calculated during execution)
        self.start_time = -1              # When process first gets CPU
        self.completion_time = 0          # When process finishes
        self.waiting_time = 0             # Time spent waiting in ready queue
        self.turnaround_time = 0          # Total time from arrival to completion
        self.response_time = -1           # Time from arrival to first execution
        
        # Memory allocation tracking
        self.memory_allocated = False     # Whether memory is allocated
        self.memory_start = -1            # Starting address in memory
        self.memory_end = -1              # Ending address in memory
        
        # Process state (NEW, READY, RUNNING, WAITING, TERMINATED)
        self.state = "NEW"
        
    def __repr__(self):
        """String representation for debugging"""
        return f"P{self.pid}(AT:{self.arrival_time}, BT:{self.burst_time}, MEM:{self.memory_required}MB)"
    
    def __lt__(self, other):
        """Less than comparison for priority queue operations"""
        return self.priority < other.priority
    
    def get_info(self):
        """Returns formatted process information"""
        return {
            'pid': self.pid,
            'arrival_time': self.arrival_time,
            'burst_time': self.burst_time,
            'memory_required': self.memory_required,
            'priority': self.priority,
            'start_time': self.start_time,
            'completion_time': self.completion_time,
            'waiting_time': self.waiting_time,
            'turnaround_time': self.turnaround_time,
            'response_time': self.response_time,
            'state': self.state
        }