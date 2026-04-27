from pylogix import PLC
import time
from django.utils import timezone
from .models import LogEntry


class PLCScanner:

    def __init__(self, ip_address, processor_slot, reporting_period=10000000):

        print("Initializing!")
        self.ip_address = ip_address
        self.processor_slot = processor_slot
        self.reporting_period = reporting_period

        self.cur_timer = 0
        self.first_scan = True
        self.cur_operating_mode = 0
        self.connection_status = True # Default to true so that it'll log an error before going bad

        self.comm = PLC()
        self.comm.IPAddress = self.ip_address
        self.comm.ProcessorSlot = self.processor_slot

        # Station states
        self.mpo_oven_has_puck = False
        self.mpo_gripper_has_puck = False
        self.mpo_turntable_has_puck = False
        self.sld_has_puck = False
        self.estop = False

        # Puck info
        self.puck_color = "Null"

        # Segment timers
        self.segment_start = {
            "oven": None,
            "gripper": None,
            "turntable": None,
            "sld": None
        }

        # Timeout limits (seconds)
        self.segment_limits = {
            "oven": 15,
            "gripper": 25,
            "turntable": 15,
            "sld": 10
        }

        # Prevent repeated timeout spam
        self.segment_timeout_reported = {
            "oven": False,
            "gripper": False,
            "turntable": False,
            "sld": False
        }

        # Total process timing
        self.process_start = None
        self.process_limit = 60
        self.process_timeout_reported = False

def Scan():
    with PLC() as comm:
        comm.IPAddress = "10.8.0.110"
        comm.ProcessorSlot = 0
        
        tags = ["Program:MainProgram.SLD_Red_Time", "Program:MainProgram.SLD_Blue_Time"]
        results = comm.Read(tags)
        
        # Check results
        output = []
        for res in results:
            if res.Status == "Success":
                output.append(res.Value)
            else:
                print(f"Error reading {res.TagName}: {res.Status}")
                output.append(None)
                
        return output

def Increment_Scores():
    with PLC() as comm:
        comm.IPAddress = "10.8.0.110"
        comm.ProcessorSlot = 0
        
        tags = ["Program:MainProgram.SLD_Red_Time", "Program:MainProgram.SLD_Blue_Time"]
        results = comm.Read(tags)
        
        write_data = []
        
        for res in results:
            if res.Status == "Success":
                new_value = res.Value + 1
                write_data.append((res.TagName, new_value))
            else:
                print(f"Read Error for {res.TagName}: {res.Status}")

        if write_data:
            write_results = comm.Write(write_data)
            
            for w_res in write_results:
                if w_res.Status != "Success":
                    print(f"Write Error for {w_res.TagName}: {w_res.Status}")
                else:
                    print(f"Successfully updated {w_res.TagName} to {w_res.Value}")


if __name__ == "__main__":
    StartScanning()
