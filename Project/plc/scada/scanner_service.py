import threading
import os
import time
from .AB_Pylogix import PLCScanner

class ScannerManager:
    _instance = None
    _lock = threading.Lock()
    start_time = time.time()

    @classmethod
    def get_scanner(cls):
        with cls._lock:
            if cls._instance is None:
                print("--- Creating Global Scanner Instance ---")
                cls._instance = PLCScanner(ip_address="10.8.0.110", processor_slot=0)
            return cls._instance

def run_scanner():
    scanner = ScannerManager.get_scanner()
    print("--- PLC Thread Started ---", flush=True)
    while True:
        try:
            scanner.scan()
        except Exception as e:
            print(f"Scanner Error: {e}", flush=True)
        
        time.sleep(0.1)

def start_scanner():
    if os.environ.get('RUN_MAIN') != 'true':
        print("Failed to open thread")
        return
        
    thread = threading.Thread(target=run_scanner, daemon=True)
    thread.start()

# Get the time since this program started
def get_elapsed_time():
    return int(time.time() - ScannerManager.start_time)