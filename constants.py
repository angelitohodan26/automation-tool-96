# constants.py for automation-tool-96
# Error codes for common edge cases
ERROR_INVALID_INPUT = 1001
ERROR_FILE_NOT_FOUND = 1002
ERROR_PERMISSION_DENIED = 1003
ERROR_TIMEOUT = 1004
ERROR_EMPTY_DATA = 1005

# Error messages mapped to codes
ERROR_MESSAGES = {
    ERROR_INVALID_INPUT: "Input data is invalid or malformed.",
    ERROR_FILE_NOT_FOUND: "The requested file does not exist.",
    ERROR_PERMISSION_DENIED: "Access to the resource is denied.",
    ERROR_TIMEOUT: "Operation timed out after waiting period.",
    ERROR_EMPTY_DATA: "Provided data is empty or missing.",
}

# Operation constants
DEFAULT_TIMEOUT = 60
MAX_RETRY_ATTEMPTS = 5
BATCH_SIZE = 100

def get_error_message(code):
    # Retrieve message or default
    return ERROR_MESSAGES.get(code, "Unknown error occurred.")

def handle_error(error_code, context=None):
    # Handle by constructing message and simulating response
    message = get_error_message(error_code)
    if context:
        message += f" Context: {context}"
    print(f"[ERROR {error_code}] {message}")
    return {"code": error_code, "message": message}

def validate_data(data):
    # Check for various edge cases in input data
    if data is None:
        return handle_error(ERROR_INVALID_INPUT, "data is None")
    if isinstance(data, str) and len(data.strip()) == 0:
        return handle_error(ERROR_EMPTY_DATA, "string is empty")
    if isinstance(data, (list, dict)) and len(data) == 0:
        return handle_error(ERROR_EMPTY_DATA, "collection is empty")
    if not isinstance(data, (str, int, float, list, dict)):
        return handle_error(ERROR_INVALID_INPUT, f"unsupported type {type(data)}")
    return {"code": 0, "message": "Data is valid."}

def safe_read_file(path):
    # Safe file read with edge case handling
    import os
    if not path or not isinstance(path, str):
        return handle_error(ERROR_INVALID_INPUT, "invalid path")
    if not os.path.exists(path):
        return handle_error(ERROR_FILE_NOT_FOUND, path)
    try:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        if not content.strip():
            return handle_error(ERROR_EMPTY_DATA, "file content empty")
        return {"code": 0, "content": content}
    except PermissionError:
        return handle_error(ERROR_PERMISSION_DENIED, path)
    except Exception as exc:
        return handle_error(ERROR_TIMEOUT, str(exc))

def with_retry(func, *args, max_attempts=MAX_RETRY_ATTEMPTS, **kwargs):
    # Wrap function with retry for transient edge cases
    for attempt in range(1, max_attempts + 1):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as exc:
            if attempt == max_attempts:
                return handle_error(ERROR_TIMEOUT, f"after {max_attempts} attempts: {exc}")
            print(f"Attempt {attempt} failed, retrying...")
    return None

# Demonstrate the error handling
if __name__ == "__main__":
    print("Automation tool error handling constants initialized")