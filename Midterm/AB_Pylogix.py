from pylogix import PLC
import time


class PLCScanner:

    def __init__(self, ip_address, processor_slot, reporting_period=10000000):

        self.ip_address = ip_address
        self.processor_slot = processor_slot
        self.reporting_period = reporting_period

        self.cur_timer = 0
        self.first_scan = True
        self.cur_operating_mode = 0

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

    # -----------------------------------------------------

    def timestamp(self):
        return time.strftime("%H:%M:%S")

    # -----------------------------------------------------

    def scan_tag(self, tag_name):

        result = self.comm.Read(tag_name)

        if result.Status == "Success":
            return result.Value

        print(f"[ERROR {self.timestamp()}] Failed to read {tag_name}. Code {result.Status}")
        return None

    # -----------------------------------------------------

    def calculate_puck_color(self):

        belt_time = self.scan_tag("Program:MainProgram.SLD_Move_Time")

        red_time = self.scan_tag("Program:MainProgram.SLD_Red_Time")
        white_time = self.scan_tag("Program:MainProgram.SLD_White_Time")
        blue_time = self.scan_tag("Program:MainProgram.SLD_Blue_Time")

        if belt_time == red_time:
            self.puck_color = "Red"

        elif belt_time == blue_time:
            self.puck_color = "Blue"

        elif belt_time == white_time:
            self.puck_color = "White"

        else:
            self.puck_color = "Null"

    # -----------------------------------------------------

    def first_scan_init(self):

        self.cur_operating_mode = self.scan_tag("Program:MainProgram.Operation_Mode")

        self.mpo_oven_has_puck = self.scan_tag("Program:MainProgram.MPO_Has_Puck")
        self.mpo_gripper_has_puck = (self.scan_tag("Program:MainProgram.Step[1]") != 0)
        self.mpo_turntable_has_puck = (self.scan_tag("Program:MainProgram.Step[2]") != 0)
        self.sld_has_puck = (self.scan_tag("Program:MainProgram.SLD_Step") != 20)

        self.estop = self.scan_tag("Program:MainProgram.ESTOP")

        print(f"[OPERATION MODE {self.timestamp()}] Initial Mode: {self.cur_operating_mode}")

    # -----------------------------------------------------

    def update_operation_mode(self):

        old_mode = self.cur_operating_mode
        self.cur_operating_mode = self.scan_tag("Program:MainProgram.Operation_Mode")

        if old_mode != self.cur_operating_mode:
            print(f"[OPERATION MODE {self.timestamp()}] Changed to {self.cur_operating_mode}")

    # -----------------------------------------------------

    def update_mpo_oven(self):

        new_state = self.scan_tag("Program:MainProgram.MPO_Has_Puck")

        if new_state and not self.mpo_oven_has_puck:

            print(f"[PROGRESS {self.timestamp()}] MPO Oven Received Puck")

            if self.process_start is None:
                self.process_start = time.time()
                self.process_timeout_reported = False

            self.segment_start["oven"] = time.time()
            self.segment_timeout_reported["oven"] = False

        elif not new_state and self.mpo_oven_has_puck:

            elapsed = time.time() - self.segment_start["oven"]
            print(f"[PROGRESS {self.timestamp()}] MPO Oven Finished Puck ({elapsed:.2f}s)")

            self.segment_start["oven"] = None

        self.mpo_oven_has_puck = new_state

    # -----------------------------------------------------

    def update_mpo_gripper(self):

        new_state = (self.scan_tag("Program:MainProgram.Step[1]") != 0)

        if new_state and not self.mpo_gripper_has_puck:

            print(f"[PROGRESS {self.timestamp()}] MPO Gripper Received Puck")

            self.segment_start["gripper"] = time.time()
            self.segment_timeout_reported["gripper"] = False

        elif not new_state and self.mpo_gripper_has_puck:

            elapsed = time.time() - self.segment_start["gripper"]
            print(f"[PROGRESS {self.timestamp()}] MPO Gripper Finished Puck ({elapsed:.2f}s)")

            self.segment_start["gripper"] = None

        self.mpo_gripper_has_puck = new_state

    # -----------------------------------------------------

    def update_mpo_turntable(self):

        new_state = (self.scan_tag("Program:MainProgram.Step[2]") != 0)

        if new_state and not self.mpo_turntable_has_puck:

            print(f"[PROGRESS {self.timestamp()}] MPO Turntable Received Puck")

            self.segment_start["turntable"] = time.time()
            self.segment_timeout_reported["turntable"] = False

        elif not new_state and self.mpo_turntable_has_puck:

            elapsed = time.time() - self.segment_start["turntable"]
            print(f"[PROGRESS {self.timestamp()}] MPO Turntable Finished Puck ({elapsed:.2f}s)")

            self.segment_start["turntable"] = None

        self.mpo_turntable_has_puck = new_state

    # -----------------------------------------------------

    def update_sld(self):

        new_state = (self.scan_tag("Program:MainProgram.SLD_Step") != 20)

        if new_state and not self.sld_has_puck:

            print(f"[PROGRESS {self.timestamp()}] SLD Received Puck")

            self.segment_start["sld"] = time.time()
            self.segment_timeout_reported["sld"] = False

        elif not new_state and self.sld_has_puck:

            elapsed = time.time() - self.segment_start["sld"]
            print(f"[PROGRESS {self.timestamp()}] SLD Finished Puck ({elapsed:.2f}s)")

            self.segment_start["sld"] = None

            self.calculate_puck_color()

            total_time = time.time() - self.process_start
            print(f"[PUCK {self.timestamp()}] {self.puck_color} Puck Processed (Total {total_time:.2f}s)")

            self.process_start = None

        self.sld_has_puck = new_state

    # -----------------------------------------------------

    def update_estop(self):

        new_estop = self.scan_tag("Program:MainProgram.ESTOP")

        if new_estop and not self.estop:
            print(f"[SAFETY {self.timestamp()}] E-STOP PRESSED")

        elif not new_estop and self.estop:
            print(f"[SAFETY {self.timestamp()}] E-STOP RELEASED")

        self.estop = new_estop

    # -----------------------------------------------------

    def check_segment_timeouts(self):

        now = time.time()

        for segment in self.segment_start:

            start = self.segment_start[segment]

            if start is None:
                continue

            elapsed = now - start
            limit = self.segment_limits[segment]

            if elapsed > limit and not self.segment_timeout_reported[segment]:

                print(f"[ERROR {self.timestamp()}] {segment.upper()} TIMEOUT ({elapsed:.2f}s > {limit}s)")

                self.segment_timeout_reported[segment] = True

    # -----------------------------------------------------

    def check_process_timeout(self):

        if self.process_start is None:
            return

        elapsed = time.time() - self.process_start

        if elapsed > self.process_limit and not self.process_timeout_reported:

            print(f"[ERROR {self.timestamp()}] PROCESS TIMEOUT ({elapsed:.2f}s > {self.process_limit}s)")

            self.process_timeout_reported = True

    # -----------------------------------------------------

    def scan(self):

        if self.first_scan:
            self.first_scan = False
            self.first_scan_init()

        self.update_estop()
        self.update_operation_mode()

        self.update_mpo_oven()
        self.update_mpo_gripper()
        self.update_mpo_turntable()
        self.update_sld()

        self.check_segment_timeouts()
        self.check_process_timeout()

    # -----------------------------------------------------

    def run(self):

        while True:

            self.cur_timer += 1

            if self.cur_timer >= self.reporting_period:

                self.cur_timer = 0
                self.scan()


# ---------------------------------------------------------

if __name__ == "__main__":

    scanner = PLCScanner(
        ip_address="10.8.0.110",
        processor_slot=0,
        reporting_period=10000000
    )

    scanner.run()