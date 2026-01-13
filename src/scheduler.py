from collections import deque
import heapq

class Scheduler:
    """
    CPU Scheduler that implements multiple scheduling algorithms.
    """
    
    def __init__(self, algorithm="FCFS", time_quantum=2):
        """
        Initialize the scheduler.
        
        Args:
            algorithm (str): Scheduling algorithm to use
            time_quantum (int): Time quantum for Round Robin
        """
        self.algorithm = algorithm
        self.time_quantum = time_quantum
        self.ready_queue = []
        self.current_time = 0
        self.completed_processes = []
        self.gantt_chart = []
        
    def add_process(self, process):
        """
        Add a process to the ready queue based on the scheduling algorithm.
        
        Args:
            process: Process object to add to ready queue
        """
        process.state = "READY"
        
        if self.algorithm == "FCFS":
            # Simple FIFO queue
            self.ready_queue.append(process)
            
        elif self.algorithm == "SJF":
            # Priority queue based on remaining time
            heapq.heappush(self.ready_queue, 
                          (process.remaining_time, process.arrival_time, process))
            
        elif self.algorithm == "Priority":
            # Priority queue based on priority value
            heapq.heappush(self.ready_queue, 
                          (process.priority, process.arrival_time, process))
            
        elif self.algorithm == "RR":
            # Simple FIFO queue (Round Robin uses time quantum)
            self.ready_queue.append(process)
    
    def get_next_process(self):
        """
        Get the next process from ready queue based on algorithm.
        
        Returns:
            Process object or None if queue is empty
        """
        if not self.ready_queue:
            return None
        
        if self.algorithm in ["SJF", "Priority"]:
            # Pop from heap (returns tuple)
            return heapq.heappop(self.ready_queue)[2]
        else:
            # Pop from regular queue (FCFS or RR)
            return self.ready_queue.pop(0)
    
    def execute(self, process, time_slice):
        """
        Execute a process for the given time slice.
        
        Args:
            process: Process to execute
            time_slice: Maximum time to execute
            
        Returns:
            bool: True if process completed, False otherwise
        """
        process.state = "RUNNING"
        
        # Record start time if this is first execution
        if process.start_time == -1:
            process.start_time = self.current_time
            process.response_time = self.current_time - process.arrival_time
        
        # Calculate actual execution time
        execution_time = min(time_slice, process.remaining_time)
        process.remaining_time -= execution_time
        self.current_time += execution_time
        
        # Add to Gantt chart
        self.gantt_chart.append({
            'pid': process.pid,
            'start': self.current_time - execution_time,
            'end': self.current_time
        })
        
        # Check if process completed
        if process.remaining_time == 0:
            process.state = "TERMINATED"
            process.completion_time = self.current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            self.completed_processes.append(process)
            return True
        
        return False
    
    def schedule(self, processes):
        """
        Main scheduling function that executes all processes.
        
        Args:
            processes: List of Process objects to schedule
            
        Returns:
            List of completed processes with calculated metrics
        """
        # Sort processes by arrival time
        all_processes = sorted(processes, key=lambda p: p.arrival_time)
        process_index = 0
        
        while process_index < len(all_processes) or self.ready_queue:
            # Add all newly arrived processes to ready queue
            while (process_index < len(all_processes) and 
                   all_processes[process_index].arrival_time <= self.current_time):
                self.add_process(all_processes[process_index])
                process_index += 1
            
            # If no process is ready, advance time to next arrival
            if not self.ready_queue:
                if process_index < len(all_processes):
                    self.current_time = all_processes[process_index].arrival_time
                continue
            
            # Get next process to execute
            current_process = self.get_next_process()
            
            # Execute based on algorithm
            if self.algorithm == "RR":
                # Round Robin: execute for time quantum
                completed = self.execute(current_process, self.time_quantum)
                if not completed:
                    # Process not finished, add back to queue
                    self.add_process(current_process)
            else:
                # Non-preemptive: execute until completion
                self.execute(current_process, current_process.remaining_time)
        
        return self.completed_processes
    
    def get_gantt_chart(self):
        """Returns the Gantt chart data"""
        return self.gantt_chart
    
    def get_total_time(self):
        """Returns total execution time"""
        return self.current_time