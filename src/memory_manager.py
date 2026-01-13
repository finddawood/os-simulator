class MemoryBlock:
    """
    Represents a block of memory.
    """
    
    def __init__(self, start, size):
        self.start = start          # Starting address
        self.size = size            # Size in MB
        self.allocated = False      # Allocation status
        self.process_id = None      # Which process owns this block
    
    def __repr__(self):
        status = f"P{self.process_id}" if self.allocated else "Free"
        end = self.start + self.size - 1
        return f"[{self.start}-{end}:{status},{self.size}MB]"


class MemoryManager:
    """
    Manages memory allocation and deallocation for processes.
    """
    
    def __init__(self, total_memory=1024, strategy="First-Fit"):
        """
        Initialize memory manager.
        
        Args:
            total_memory (int): Total memory size in MB
            strategy (str): Allocation strategy to use
        """
        self.total_memory = total_memory
        self.strategy = strategy
        # Initially, all memory is one free block
        self.memory_blocks = [MemoryBlock(0, total_memory)]
        self.allocated_blocks = {}  # Map process_id to MemoryBlock
    
    def allocate(self, process):
        """
        Allocate memory for a process using the selected strategy.
        
        Args:
            process: Process object needing memory
            
        Returns:
            bool: True if allocation successful, False otherwise
        """
        size_needed = process.memory_required
        
        # Find suitable block using selected strategy
        suitable_block = None
        
        if self.strategy == "First-Fit":
            suitable_block = self._first_fit(size_needed)
        elif self.strategy == "Best-Fit":
            suitable_block = self._best_fit(size_needed)
        elif self.strategy == "Worst-Fit":
            suitable_block = self._worst_fit(size_needed)
        
        if suitable_block:
            # Allocate memory to process
            process.memory_allocated = True
            process.memory_start = suitable_block.start
            process.memory_end = suitable_block.start + size_needed - 1
            
            # Split block if it's larger than needed
            if suitable_block.size > size_needed:
                # Create new free block with remaining space
                new_block = MemoryBlock(
                    suitable_block.start + size_needed,
                    suitable_block.size - size_needed
                )
                block_index = self.memory_blocks.index(suitable_block)
                self.memory_blocks.insert(block_index + 1, new_block)
            
            # Update the allocated block
            suitable_block.size = size_needed
            suitable_block.allocated = True
            suitable_block.process_id = process.pid
            self.allocated_blocks[process.pid] = suitable_block
            
            return True
        
        return False
    
    def deallocate(self, process):
        """
        Deallocate memory for a process.
        
        Args:
            process: Process whose memory should be freed
            
        Returns:
            bool: True if deallocation successful, False otherwise
        """
        if process.pid not in self.allocated_blocks:
            return False
        
        # Free the memory block
        block = self.allocated_blocks[process.pid]
        block.allocated = False
        block.process_id = None
        del self.allocated_blocks[process.pid]
        
        # Merge adjacent free blocks to reduce fragmentation
        self._merge_free_blocks()
        
        process.memory_allocated = False
        return True
    
    def _first_fit(self, size):
        """
        First-Fit: Allocate first block that's large enough.
        
        Args:
            size: Required memory size
            
        Returns:
            MemoryBlock or None
        """
        for block in self.memory_blocks:
            if not block.allocated and block.size >= size:
                return block
        return None
    
    def _best_fit(self, size):
        """
        Best-Fit: Allocate smallest block that's large enough.
        
        Args:
            size: Required memory size
            
        Returns:
            MemoryBlock or None
        """
        best_block = None
        min_size_diff = float('inf')
        
        for block in self.memory_blocks:
            if not block.allocated and block.size >= size:
                size_diff = block.size - size
                if size_diff < min_size_diff:
                    min_size_diff = size_diff
                    best_block = block
        
        return best_block
    
    def _worst_fit(self, size):
        """
        Worst-Fit: Allocate largest available block.
        
        Args:
            size: Required memory size
            
        Returns:
            MemoryBlock or None
        """
        worst_block = None
        max_size = -1
        
        for block in self.memory_blocks:
            if not block.allocated and block.size >= size:
                if block.size > max_size:
                    max_size = block.size
                    worst_block = block
        
        return worst_block
    
    def _merge_free_blocks(self):
        """
        Merge adjacent free memory blocks to reduce fragmentation.
        """
        i = 0
        while i < len(self.memory_blocks) - 1:
            current = self.memory_blocks[i]
            next_block = self.memory_blocks[i + 1]
            
            # If both blocks are free and adjacent, merge them
            if not current.allocated and not next_block.allocated:
                current.size += next_block.size
                self.memory_blocks.pop(i + 1)
            else:
                i += 1
    
    def get_fragmentation(self):
        """
        Calculate external fragmentation percentage.
        
        Returns:
            float: Fragmentation percentage
        """
        free_blocks = [b for b in self.memory_blocks if not b.allocated]
        
        if not free_blocks:
            return 0.0
        
        total_free = sum(b.size for b in free_blocks)
        largest_free = max(b.size for b in free_blocks) if free_blocks else 0
        
        if total_free == 0:
            return 0.0
        
        # Fragmentation = (total_free - largest_free) / total_free * 100
        fragmentation = ((total_free - largest_free) / total_free) * 100
        return fragmentation
    
    def get_utilization(self):
        """
        Calculate memory utilization percentage.
        
        Returns:
            float: Utilization percentage
        """
        used_memory = sum(b.size for b in self.memory_blocks if b.allocated)
        return (used_memory / self.total_memory) * 100
    
    def get_memory_state(self):
        """
        Get current memory state as string.
        
        Returns:
            str: Memory blocks representation
        """
        return " | ".join(str(block) for block in self.memory_blocks)
    
    def __repr__(self):
        return self.get_memory_state()