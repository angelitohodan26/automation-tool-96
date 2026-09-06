import sys

def validate_input(data):
    """Ensures input is a non-empty string under 256 chars."""
    if not isinstance(data, str) or len(data.strip()) == 0:
        return False
    if len(data) > 256:
        return False
    return True

def process_data(value):
    """Example processing logic."""
    return f"processed: {value.upper()}"

def main_loop():
    """Main execution loop for automation-tool-96."""
    print("Starting processing loop. Type 'exit' to quit.")
    
    while True:
        user_input = input(">> ").strip()
        
        if user_input.lower() == 'exit':
            print("Shutting down.")
            break
            
        if not validate_input(user_input):
            print("Error: Invalid input format. Please try again.")
            continue
            
        try:
            result = process_data(user_input)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Critical processing error: {e}")

if __name__ == "__main__":
    main_loop()