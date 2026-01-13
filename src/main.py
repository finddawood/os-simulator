from process import Process
from scheduler import Scheduler
from memory_manager import MemoryManager
from metrics import Metrics
from utils import *
import sys

def display_main_menu():
    """Display the main menu options"""
    print_header("OS PROCESS & MEMORY MANAGEMENT SIMULATOR")
    print("\n📋 MAIN MENU")
    print_separator()
    print("1. Run Predefined Test Case")
    print("2. Input Custom Processes")
    print("3. Load Processes from File")
    print("4. View Documentation")
    print("5. Exit")
    print_separator()

def get_scheduling_algorithm():
    """
    Get scheduling algorithm selection from user.
    
    Returns:
        tuple: (algorithm_name, time_quantum)
    """
    print("\n⚙️  SELECT SCHEDULING ALGORITHM")
    print_separator()
    print("1. FCFS (First-Come-First-Serve)")
    print("2. SJF (Shortest Job First)")
    print("3. Priority Scheduling")
    print("4. Round Robin")
    print_separator()
    
    choice = get_choice("Enter choice (1-4): ", ['1', '2', '3', '4'])
    
    algorithms = {
        '1': 'FCFS',
        '2': 'SJF',
        '3': 'Priority',
        '4': 'RR'
    }
    
    algorithm = algorithms[choice]
    time_quantum = 0
    
    # Get time quantum for Round Robin
    if algorithm == 'RR':
        time_quantum = get_positive_int("Enter time quantum: ", min_value=1)
    
    return algorithm, time_quantum

def get_memory_strategy():
    """
    Get memory allocation strategy from user.
    
    Returns:
        str: Memory allocation strategy name
    """
    print("\n💾 SELECT MEMORY ALLOCATION STRATEGY")
    print_separator()
    print("1. First-Fit")
    print("2. Best-Fit")
    print("3. Worst-Fit")
    print_separator()
    
    choice = get_choice("Enter choice (1-3): ", ['1', '2', '3'])
    
    strategies = {
        '1': 'First-Fit',
        '2': 'Best-Fit',
        '3': 'Worst-Fit'
    }
    
    return strategies[choice]

def create_predefined_processes():
    """
    Create a predefined set of test processes.
    
    Returns:
        list: List of Process objects
    """
    return [
        Process(pid=1, arrival_time=0, burst_time=8, memory_required=100, priority=2),
        Process(pid=2, arrival_time=1, burst_time=4, memory_required=200, priority=1),
        Process(pid=3, arrival_time=2, burst_time=9, memory_required=150, priority=3),
        Process(pid=4, arrival_time=3, burst_time=5, memory_required=250, priority=2),
        Process(pid=5, arrival_time=4, burst_time=3, memory_required=100, priority=1)
    ]

def input_custom_processes():
    """
    Get custom process specifications from user.
    
    Returns:
        list: List of Process objects
    """
    print("\n➕ CUSTOM PROCESS INPUT")
    print_separator()
    
    try:
        n = get_positive_int("Enter number of processes: ", min_value=1)
        processes = []
        
        for i in range(n):
            print(f"\n📝 Process {i+1} Details:")
            arrival = get_positive_int("  Arrival Time: ", min_value=0)
            burst = get_positive_int("  Burst Time: ", min_value=1)
            memory = get_positive_int("  Memory Required (MB): ", min_value=1)
            priority = get_positive_int("  Priority (lower = higher priority): ", min_value=0)
            
            processes.append(Process(i+1, arrival, burst, memory, priority))
        
        print(f"\n✓ Successfully created {n} processes")
        return processes
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Input cancelled. Using predefined processes.")
        return create_predefined_processes()

def load_processes_from_file(filename):
    """
    Load process specifications from a text file.
    
    File format (one process per line):
    arrival_time burst_time memory_required priority
    
    Args:
        filename: Path to the input file
        
    Returns:
        list: List of Process objects
    """
    processes = []
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            pid = 1
            
            for line in lines:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    parts = line.split()
                    if len(parts) >= 4:
                        arrival = int(parts[0])
                        burst = int(parts[1])
                        memory = int(parts[2])
                        priority = int(parts[3])
                        processes.append(Process(pid, arrival, burst, memory, priority))
                        pid += 1
        
        if processes:
            print(f"✓ Successfully loaded {len(processes)} processes from file")
            return processes
        else:
            print("⚠️  No valid processes found in file. Using predefined processes.")
            return create_predefined_processes()
    
    except FileNotFoundError:
        print(f"✗ File '{filename}' not found! Using predefined processes.")
        return create_predefined_processes()
    except Exception as e:
        print(f"✗ Error reading file: {e}. Using predefined processes.")
        return create_predefined_processes()

def run_simulation(processes, algorithm, time_quantum, memory_strategy, total_memory):
    """
    Run the complete OS simulation.
    
    Args:
        processes: List of Process objects
        algorithm: Scheduling algorithm name
        time_quantum: Time quantum for Round Robin
        memory_strategy: Memory allocation strategy
        total_memory: Total memory size in MB
    """
    print_header("SIMULATION STARTED")
    
    # Display simulation configuration
    print(f"\n📊 Configuration:")
    print(f"  • Scheduling Algorithm: {algorithm}")
    if algorithm == 'RR':
        print(f"  • Time Quantum: {time_quantum}")
    print(f"  • Memory Strategy: {memory_strategy}")
    print(f"  • Total Memory: {total_memory} MB")
    print(f"  • Number of Processes: {len(processes)}")
    
    # Initialize scheduler and memory manager
    scheduler = Scheduler(algorithm, time_quantum)
    memory_manager = MemoryManager(total_memory, memory_strategy)
    
    # Phase 1: Memory Allocation
    print("\n" + "="*80)
    print(" " * 30 + "PHASE 1: MEMORY ALLOCATION")
    print("="*80)
    
    for process in processes:
        if memory_manager.allocate(process):
            print(f"✓ Process P{process.pid}: Allocated {process.memory_required}MB "
                  f"at [{process.memory_start}-{process.memory_end}]")
        else:
            print(f"✗ Process P{process.pid}: Failed to allocate {process.memory_required}MB "
                  f"(Insufficient memory)")
    
    print(f"\n💾 Memory State: {memory_manager}")
    
    # Get only processes that got memory allocated
    allocated_processes = [p for p in processes if p.memory_allocated]
    
    if not allocated_processes:
        print("\n⚠️  No processes could be allocated memory. Simulation terminated.")
        return
    
    # Phase 2: CPU Scheduling
    print("\n" + "="*80)
    print(" " * 30 + "PHASE 2: CPU SCHEDULING")
    print("="*80)
    
    completed = scheduler.schedule(allocated_processes)
    
    # Phase 3: Display Results
    print("\n" + "="*80)
    print(" " * 32 + "PHASE 3: RESULTS")
    print("="*80)
    
    # Display process execution details
    Metrics.display_process_table(completed)
    
    # Display Gantt chart
    Metrics.display_gantt_chart(scheduler.get_gantt_chart())
    
    # Display memory allocation
    Metrics.display_memory_allocation(completed, memory_manager)
    
    # Calculate and display performance metrics
    metrics = Metrics.calculate_average_metrics(completed)
    cpu_util = Metrics.calculate_cpu_utilization(scheduler.get_gantt_chart(), 
                                                   scheduler.get_total_time())
    memory_util = memory_manager.get_utilization()
    fragmentation = memory_manager.get_fragmentation()
    
    Metrics.display_summary(metrics, cpu_util, memory_util, fragmentation)
    
    # Phase 4: Memory Deallocation
    print("\n" + "="*80)
    print(" " * 27 + "PHASE 4: MEMORY DEALLOCATION")
    print("="*80)
    
    for process in completed:
        if memory_manager.deallocate(process):
            print(f"✓ Process P{process.pid}: Memory deallocated")
    
    print(f"\n💾 Final Memory State: {memory_manager}")
    
    print_header("SIMULATION COMPLETED SUCCESSFULLY")

def display_documentation():
    """Display project documentation and help"""
    clear_screen()
    print_header("DOCUMENTATION")
    
    print("\n📖 ABOUT THIS PROJECT")
    print_separator()
    print("This Operating System Simulator implements:")
    print("  • Process Management with multiple scheduling algorithms")
    print("  • Memory Management with various allocation strategies")
    print("  • Performance metric calculation and analysis")
    print()
    print("🎯 SCHEDULING ALGORITHMS:")
    print("  • FCFS: Processes executed in arrival order")
    print("  • SJF: Shortest process executed first")
    print("  • Priority: Higher priority processes execute first")
    print("  • Round Robin: Time-sharing with time quantum")
    print()
    print("💾 MEMORY STRATEGIES:")
    print("  • First-Fit: Allocate first suitable block")
    print("  • Best-Fit: Allocate smallest suitable block")
    print("  • Worst-Fit: Allocate largest suitable block")
    print()
    print("📊 PERFORMANCE METRICS:")
    print("  • Waiting Time: Time spent in ready queue")
    print("  • Turnaround Time: Total time from arrival to completion")
    print("  • Response Time: Time from arrival to first execution")
    print("  • CPU Utilization: Percentage of CPU busy time")
    print("  • Throughput: Processes completed per time unit")
    print_separator()
    
    pause()

def main():
    """Main program entry point"""
    
    try:
        while True:
            clear_screen()
            display_main_menu()
            
            choice = get_choice("\nEnter your choice: ", ['1', '2', '3', '4', '5'])
            
            if choice == '1':
                # Predefined test case
                clear_screen()
                print_header("PREDEFINED TEST CASE")
                processes = create_predefined_processes()
                
                print("\n📋 Processes loaded:")
                for p in processes:
                    print(f"  {p}")
                
                algorithm, time_quantum = get_scheduling_algorithm()
                memory_strategy = get_memory_strategy()
                total_memory = get_positive_int("\n💾 Enter total memory size (MB): ", min_value=100)
                
                clear_screen()
                run_simulation(processes, algorithm, time_quantum, memory_strategy, total_memory)
                pause()
            
            elif choice == '2':
                # Custom process input
                clear_screen()
                processes = input_custom_processes()
                algorithm, time_quantum = get_scheduling_algorithm()
                memory_strategy = get_memory_strategy()
                total_memory = get_positive_int("\n💾 Enter total memory size (MB): ", min_value=100)
                
                clear_screen()
                run_simulation(processes, algorithm, time_quantum, memory_strategy, total_memory)
                pause()
            
            elif choice == '3':
                # Load from file
                clear_screen()
                print_header("LOAD FROM FILE")
                filename = input("\n📁 Enter filename (e.g., test_cases.txt): ").strip()
                
                # Try both absolute and relative paths
                if not filename.startswith('/') and not filename.startswith('../'):
                    # Try in tests directory
                    test_filename = f"../tests/{filename}"
                    processes = load_processes_from_file(test_filename)
                else:
                    processes = load_processes_from_file(filename)
                
                algorithm, time_quantum = get_scheduling_algorithm()
                memory_strategy = get_memory_strategy()
                total_memory = get_positive_int("\n💾 Enter total memory size (MB): ", min_value=100)
                
                clear_screen()
                run_simulation(processes, algorithm, time_quantum, memory_strategy, total_memory)
                pause()
            
            elif choice == '4':
                # Documentation
                display_documentation()
            
            elif choice == '5':
                # Exit
                clear_screen()
                print_header("THANK YOU!")
                print("\n✓ Exiting OS Simulator...")
                sys.exit(0)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Program interrupted by user.")
        print("✓ Exiting gracefully...\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ An unexpected error occurred: {e}")
        print("✓ Please restart the program.\n")
        sys.exit(1)


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                                                                       ║
    ║       OPERATING SYSTEM PROCESS & MEMORY MANAGEMENT SIMULATOR          ║
    ║                                                                       ║
    ║                    Developed by: Dawood                               ║
    ║                                                                       ║
    ║                                                                       ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """)
    pause()
    main()