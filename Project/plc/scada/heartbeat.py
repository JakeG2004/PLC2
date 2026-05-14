from pylogix import PLC

def Increment_Heartbeat():
    with PLC() as comm:
        comm.IPAddress = "10.8.0.110"
        comm.ProcessorSlot = 0
        
        tags = ["Program:Heartbeat.HeartbeatCurrent"]
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
    Increment_Heartbeat()