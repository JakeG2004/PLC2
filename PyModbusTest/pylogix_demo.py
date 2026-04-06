from pylogix import PLC

# Single tag reading
with PLC() as comm:
    comm.IPAddress = '10.0.8.110'
    comm.ProcessorSlot = 0

    # Read a tag
    results = comm.Read('MyTagName')
    if(results.Status == "Success"):
        print(f"Value: {results.Value}")
    else:
        print("Failed to get tag")

    # Write a tag
    comm.Write('TagToUpdate', 42)

    # Read 10 elements out of MyDintArray
    results2 = comm.Read("MyDintArray[0]", 10)

    # Read multiple tags
    tags = ['MyTag1', 'MyTag2', 'MyTag3']

    results = comm.Read(tags)

    for result in results:
        if(result.Status == "Success"):
            print(f"Value of tag {result.TagName}: {result.Value}")
        else:
            print("Failed to connect")

    # Discover what tags are on the device
    tags = comm.GetTagList()
    time = comm.GetPLCTime()