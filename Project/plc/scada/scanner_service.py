# scanner_service.py
import threading
import time
from .AB_Pylogix import PLCScanner

scanner_instance = PLCScanner(ip_address="10.8.0.110", processor_slot=0)
scanner_instance.log_buffer = []

# Use a Lock to prevent race conditions during startup
_lock = threading.Lock()
is_scanning = False

def run_scanner():
    while True:
        try:
            scanner_instance.scan()
        except Exception as e:
            print(f"Scanner Error: {e}")
        time.sleep(0.5)

def start_scanner():
    global is_scanning
    with _lock:
        if is_scanning:
            return  # Already running
        
        is_scanning = True
        thread = threading.Thread(target=run_scanner, name="PLCScannerThread", daemon=True)
        thread.start()
        print("--- PLC Scanner Thread Started ---")