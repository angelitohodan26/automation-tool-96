import multiprocessing

# performance configuration constants
# utilizing cpu count to optimize parallel execution

CACHE_SIZE_LIMIT = 1024
WORKER_POOL_SIZE = max(1, multiprocessing.cpu_count() - 1)
BATCH_PROCESSING_TIMEOUT = 30

# memory optimization thresholds
MEMORY_THRESHOLD_MB = 512
GC_COLLECTION_INTERVAL = 100

# performance related feature flags
ENABLE_COMPRESSION = True
USE_ASYNC_IO = True

def get_optimized_batch_size(item_count: int) -> int:
    """calculate batch size based on available resources."""
    if item_count < 1000:
        return item_count
    return max(100, item_count // WORKER_POOL_SIZE)

# metadata for the automation tool
SUPPORTED_PLATFORMS = ['linux', 'windows', 'darwin']
MAX_RETRIES = 3