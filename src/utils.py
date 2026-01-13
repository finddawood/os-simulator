def clear_screen():
    """Clear the console screen (cross-platform)"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*80)
    padding = (80 - len(text)) // 2
    print(" " * padding + text)
    print("="*80)

def print_separator():
    """Print separator line"""
    print("-" * 80)

def get_positive_int(prompt, min_value=1):
    """
    Get positive integer input from user with validation.
    
    Args:
        prompt: Input prompt text
        min_value: Minimum acceptable value
        
    Returns:
        int: Valid positive integer
    """
    while True:
        try:
            value = int(input(prompt))
            if value >= min_value:
                return value
            print(f"Error: Please enter a value >= {min_value}")
        except ValueError:
            print("Error: Please enter a valid integer")

def get_choice(prompt, valid_choices):
    """
    Get user choice with validation.
    
    Args:
        prompt: Input prompt text
        valid_choices: List of valid choice strings
        
    Returns:
        str: Valid choice
    """
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print(f"Error: Please enter one of {valid_choices}")

def pause():
    """Pause execution until user presses Enter"""
    input("\nPress Enter to continue...")

def format_time(seconds):
    """
    Format time in seconds to readable string.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        str: Formatted time string
    """
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes} minutes {secs} seconds"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours} hours {minutes} minutes"