def leftPopFromList(list):
    return (list[0], list[1:])

iotaCounter= 0

def iota(resetCounter= False):

    global iotaCounter
    if(resetCounter):
        iotaCounter= 0

    currentValue= iotaCounter
    iotaCounter += 1

    return currentValue