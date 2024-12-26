import json


with open('processes.json', "r") as file:
    processes = json.load(file)


q = processes["quantum"]
processes = list(processes["processes_list"])  # processes must be sorted based on their arrival time


class PCB:
    def __init__(self, tat, waiting_t, start_t, finish_t, name):
        self.tat = tat
        self.waiting_t = waiting_t
        self.finish_t = finish_t
        self.name = name
        self.start_t = start_t

    def __str__(self):
        return f"{self.name} => start time={self.start_t}, finish time={self.finish_t}, waiting time={self.waiting_t}, TAT={self.tat}"


def total_CPU_burst(processesList):
    count = 0
    for process in processesList:
        count += process["cpu_burst"]

    return count


def FirstComeFirstServed():
    readyQueue = processes.copy()
    result = []
    tcpub = total_CPU_burst(readyQueue)

    waiting_t = 0
    finish_t = 0
    start_t = 0

    currentTime = 0
    while readyQueue.__len__():

        if readyQueue[0]["arrival_time"] <= currentTime:

            start_t = currentTime
            waiting_t = currentTime - readyQueue[0]["arrival_time"]
            
            while readyQueue[0]["cpu_burst"]:
                currentTime += 1
                readyQueue[0]["cpu_burst"] = readyQueue[0]["cpu_burst"] - 1
            
            finish_t = currentTime

            process = PCB(finish_t - readyQueue[0]["arrival_time"], waiting_t, start_t, finish_t, readyQueue[0]["name"])
            result.append(process)

            del readyQueue[0]
        else:
            currentTime += 1

    cpuUtilization = tcpub / finish_t * 100

    return [cpuUtilization, result]


def calculateWaitingTime(lastAppearanceOfEachPorcess, process, start_t, finish_t):
    waiting_t = 0

    if lastAppearanceOfEachPorcess.get(process["name"]) == None :
        lastAppearanceOfEachPorcess[process["name"]] = finish_t
        waiting_t = start_t - process["arrival_time"]
    else:
        waiting_t = start_t - lastAppearanceOfEachPorcess[process["name"]]
        lastAppearanceOfEachPorcess[process["name"]] = finish_t

    return waiting_t


def RoundRobin():
    processesList = processes.copy()
    readyQueue = []
    result = []
    lastAppearanceOfEachPorcess = dict()
    tcpub = total_CPU_burst(processesList)

    waiting_t = 0
    finish_t = 0
    start_t = 0

    currentTime = 0
    while True:
        if processesList.__len__() and processesList[0]["arrival_time"] <= currentTime:
            readyQueue.append(processesList[0])
            del processesList[0]
        elif readyQueue.__len__():
            start_t = currentTime

            for i in range(q):
                readyQueue[0]["cpu_burst"] = readyQueue[0]["cpu_burst"] - 1
                currentTime += 1

                while processesList.__len__() and processesList[0]["arrival_time"] <= currentTime:
                    readyQueue.append(processesList[0])
                    del processesList[0]

                if readyQueue[0]["cpu_burst"] == 0 : break
            
            finish_t = currentTime

            waiting_t = calculateWaitingTime(lastAppearanceOfEachPorcess, readyQueue[0], start_t, finish_t)

            process = PCB(finish_t - readyQueue[0]["arrival_time"],waiting_t, start_t, finish_t, readyQueue[0]["name"])
            result.append(process)

            if readyQueue[0]["cpu_burst"] == 0 :
                readyQueue.pop(0)
            else: 
                readyQueue.append(readyQueue.pop(0))
        else: currentTime += 1

        if readyQueue.__len__() == 0 and processesList.__len__() == 0 : break

        
    cpuUtilization = tcpub / finish_t * 100

    return [cpuUtilization, result]


def getShortestBurstTimeProcessIndex(processesList):
    index = 0
    shortest = processesList[index]
    for i in range(processesList.__len__()):
        process = processesList[i]
        if process["cpu_burst"] < shortest["cpu_burst"]:
            shortest = process
            index = i

    return index


def ShortestRemainingTime():
    processesList = processes.copy()   
    readyQueue = []
    result = []
    lastAppearanceOfEachPorcess = dict()
    tcpub = total_CPU_burst(processesList)

    waiting_t = 0
    finish_t = 0
    start_t = 0

    currentTime = 0
    while True:
        if processesList.__len__() and processesList[0]["arrival_time"] <= currentTime:
            readyQueue.append(processesList[0])
            del processesList[0]
        elif readyQueue.__len__():
            start_t = currentTime
            currentProcessIndex = getShortestBurstTimeProcessIndex(readyQueue)
            currentProcess = readyQueue[currentProcessIndex]

            while currentProcess["cpu_burst"] != 0:
                currentProcess["cpu_burst"] = currentProcess["cpu_burst"] - 1
                currentTime += 1

                while processesList.__len__() and processesList[0]["arrival_time"] == currentTime:
                    finish_t = currentTime

                    waiting_t = calculateWaitingTime(lastAppearanceOfEachPorcess, currentProcess, start_t, finish_t)

                    process = PCB(finish_t - currentProcess["arrival_time"],waiting_t, start_t, finish_t, currentProcess["name"])
                    result.append(process)

                    readyQueue.append(processesList[0])
                    del processesList[0]

                    lastProcessName = currentProcess["name"]
                    currentProcessIndex = getShortestBurstTimeProcessIndex(readyQueue)
                    currentProcess = readyQueue[currentProcessIndex]

                    if lastProcessName == currentProcess["name"]:
                        result.pop()
                        del lastAppearanceOfEachPorcess[currentProcess["name"]]
                    else: start_t = currentTime
            
            finish_t = currentTime
            
            waiting_t = calculateWaitingTime(lastAppearanceOfEachPorcess, currentProcess, start_t, finish_t)

            process = PCB(finish_t - currentProcess["arrival_time"],waiting_t, start_t, finish_t, currentProcess["name"])
            result.append(process)
            
            del readyQueue[currentProcessIndex]
            
        else:
            currentTime += 1
    
        if readyQueue.__len__() == 0 and processesList.__len__() == 0: break

    cpuUtilization = tcpub / finish_t * 100

    return [cpuUtilization, result]

print("There Are 3 Algorithms :")
print("1- First-Come First-Served")
print("2- RoundRobin")
print("3- Shortest Remaining Time First")

chosenAlgo = int(input("Enter Number Of Algorithm You Want To Apply: "))

if chosenAlgo == 1:
    result = FirstComeFirstServed()
elif chosenAlgo == 2:
    result = RoundRobin()
elif chosenAlgo == 3:
    result = ShortestRemainingTime()
else: 
    print("Invalid Number !!")

if chosenAlgo in [1,2,3]:   
    processesStats = dict()

    print("\nGantt Chart: ")
    for process in result[1]:
        if processesStats.get(process.name) == None:
            processesStats[process.name] = f"{process.tat},{process.waiting_t}"
        else:
            previousWT = int(processesStats[process.name].split(",")[1])
            processesStats[process.name] = f"{process.tat},{process.waiting_t + previousWT}"
        print(str(process))
    
    print("\n")
    for processName in processesStats.keys():
        print(f"{processName} => TAT={processesStats[processName].split(",")[0]} , Waiting Time= {processesStats[processName].split(",")[1]}")
        
    print("\nCPU Utilization: " + str(result[0]))