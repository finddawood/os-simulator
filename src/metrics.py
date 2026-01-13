class Metrics:
    """
    Static class for calculating and displaying performance metrics.
    """
    
    @staticmethod
    def calculate_average_metrics(processes):
        """
        Calculate average performance metrics for completed processes.
        
        Args:
            processes: List of completed Process objects
            
        Returns:
            dict: Dictionary containing average metrics
        """
        if not processes:
            return None
        
        n = len(processes)
        total_waiting = sum(p.waiting_time for p in processes)
        total_turnaround = sum(p.turnaround_time for p in processes)
        total_response = sum(p.response_time for p in processes)
        max_completion = max(p.completion_time for p in processes)
        
        return {
            'avg_waiting_time': total_waiting / n,
            'avg_turnaround_time': total_turnaround / n,
            'avg_response_time': total_response / n,
            'throughput': n / max_completion if max_completion > 0 else 0
        }
    
    @staticmethod
    def calculate_cpu_utilization(gantt_chart, total_time):
        """
        Calculate CPU utilization percentage.
        
        Args:
            gantt_chart: List of execution entries
            total_time: Total simulation time
            
        Returns:
            float: CPU utilization percentage
        """
        if not gantt_chart or total_time == 0:
            return 0.0
        
        busy_time = sum(entry['end'] - entry['start'] for entry in gantt_chart)
        return (busy_time / total_time) * 100
    
    @staticmethod
    def display_process_table(processes):
        """
        Display detailed process execution table.
        
        Args:
            processes: List of completed processes
        """
        print("\n" + "="*110)
        print(" " * 40 + "PROCESS EXECUTION DETAILS")
        print("="*110)
        
        # Header
        header = f"{'PID':<6} {'Arrival':<10} {'Burst':<10} {'Memory':<10} {'Start':<10} " \
                 f"{'Complete':<12} {'Waiting':<10} {'TAT':<10} {'Response':<10}"
        print(header)
        print("-"*110)
        
        # Process data rows
        for p in sorted(processes, key=lambda x: x.pid):
            row = f"{p.pid:<6} {p.arrival_time:<10} {p.burst_time:<10} " \
                  f"{p.memory_required:<10} {p.start_time:<10} {p.completion_time:<12} " \
                  f"{p.waiting_time:<10} {p.turnaround_time:<10} {p.response_time:<10}"
            print(row)
        
        print("="*110)
    
    @staticmethod
    def display_gantt_chart(gantt_chart):
        """
        Display Gantt chart visualization.
        
        Args:
            gantt_chart: List of execution entries
        """
        if not gantt_chart:
            return
        
        print("\n" + "="*80)
        print(" " * 32 + "GANTT CHART")
        print("="*80)
        
        # Print process execution blocks
        print("|", end="")
        for entry in gantt_chart:
            duration = entry['end'] - entry['start']
            # Limit width for very long durations
            width = min(duration * 3, 15)
            pid_str = f" P{entry['pid']} "
            print(f"{pid_str:^{width}}", end="|")
        print()
        
        # Print time markers
        print(gantt_chart[0]['start'], end="")
        for entry in gantt_chart:
            duration = entry['end'] - entry['start']
            width = min(duration * 3, 15)
            time_str = str(entry['end'])
            padding = " " * (width - len(time_str))
            print(padding + time_str, end="")
        print("\n" + "="*80)
    
    @staticmethod
    def display_memory_allocation(processes, memory_manager):
        """
        Display memory allocation details.
        
        Args:
            processes: List of processes
            memory_manager: MemoryManager object
        """
        print("\n" + "="*80)
        print(" " * 28 + "MEMORY ALLOCATION STATUS")
        print("="*80)
        
        for process in processes:
            if process.memory_allocated:
                status = f"✓ ALLOCATED: [{process.memory_start}-{process.memory_end}]"
                print(f"Process P{process.pid}: {status} ({process.memory_required}MB)")
            else:
                print(f"Process P{process.pid}: ✗ NOT ALLOCATED ({process.memory_required}MB)")
        
        print(f"\nMemory State: {memory_manager}")
        print("="*80)
    
    @staticmethod
    def display_summary(metrics, cpu_util, memory_util, fragmentation):
        """
        Display comprehensive performance summary.
        
        Args:
            metrics: Dictionary of average metrics
            cpu_util: CPU utilization percentage
            memory_util: Memory utilization percentage
            fragmentation: Memory fragmentation percentage
        """
        print("\n" + "="*80)
        print(" " * 25 + "PERFORMANCE METRICS SUMMARY")
        print("="*80)
        
        print(f"\n{'Metric':<35} {'Value':<20}")
        print("-"*55)
        print(f"{'Average Waiting Time':<35} {metrics['avg_waiting_time']:<20.2f} time units")
        print(f"{'Average Turnaround Time':<35} {metrics['avg_turnaround_time']:<20.2f} time units")
        print(f"{'Average Response Time':<35} {metrics['avg_response_time']:<20.2f} time units")
        print(f"{'Throughput':<35} {metrics['throughput']:<20.4f} processes/unit")
        print(f"{'CPU Utilization':<35} {cpu_util:<20.2f} %")
        print(f"{'Memory Utilization':<35} {memory_util:<20.2f} %")
        print(f"{'External Fragmentation':<35} {fragmentation:<20.2f} %")
        
        print("="*80)