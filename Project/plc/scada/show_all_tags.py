from pylogix import PLC

def list_plc_tags(ip_address, slot=0):
    """
    Connects to the PLC and prints all available tag names, 
    their data types, and whether they are arrays.
    """
    print(f"Connecting to PLC at {ip_address}...")
    
    with PLC() as comm:
        comm.IPAddress = ip_address
        comm.ProcessorSlot = slot
        
        # GetTagList returns a list of Tag objects
        tags = comm.GetTagList()
        
        if tags.Status == "Success":
            print(f"\nSuccessfully retrieved {len(tags.Value)} tags:\n")
            print(f"{'Tag Name':<40} | {'Data Type':<15} | {'Array Size'}")
            print("-" * 75)
            
            for tag in tags.Value:
                # tag.TagName, tag.DataType, and tag.Array are the main attributes
                print(f"{tag.TagName:<40} | {tag.DataType:<15} | {tag.Array}")
            
            print(f"\nTotal tags found: {len(tags.Value)}")
        else:
            print(f"Failed to retrieve tags: {tags.Status}")

if __name__ == "__main__":
    # Using your specific PLC details
    PLC_IP = "10.8.0.110"
    PLC_SLOT = 0
    
    list_plc_tags(PLC_IP, PLC_SLOT)