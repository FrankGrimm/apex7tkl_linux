from os import system
import time
import socket
import getpass
import struct

class subMemory:
    free: float
    total: float
    cached: float
    def __init__(self, free: float, total: float, cached: float):
        self.free = free / 1000000
        self.total = total / 1000000
        self.cached = cached / 1000000
        return
    def toString(self) -> str:
        return format(self.total - self.free, ".1f") + "G/" + format(self.total, ".1f") + "G"

class memory:
    ram: subMemory
    swap: subMemory
    def __init__(self):
        content = {}
        with open("/proc/meminfo") as file:
            for line in file:
                (key, val) = line.split(": ")
                tmp = val.split(" ")
                content[key] = int(tmp[tmp.count("")])
        self.ram = subMemory(content["MemFree"], content["MemTotal"], content["Cached"])
        self.swap = subMemory(content["SwapFree"], content["SwapTotal"], content["SwapCached"])
        return
    def toString(self) -> str:
        return "ram: " + self.ram.toString() + " - swp: " + self.swap.toString()

class subCpu:
    user: int
    nice: int
    system: int
    idle: int
    iowait: int
    irq: int
    softirq: int
    load1: int
    load2: int

    def __init__(self, user, nice, system, idle, iowait, irq, softirq, load1, load2) -> None:
        self.user = user
        self.nice = nice
        self.system = system
        self.idle = idle
        self.iowait = iowait
        self.irq = irq
        self.softirq = softirq
        self.load1 = load1
        self.load2 = load2
        return

    def initWith(self, tmp) -> None:
        self.user = int(tmp[0])
        self.nice = int(tmp[1])
        self.system = int(tmp[2])
        self.idle = int(tmp[3])
        self.iowait = int(tmp[4])
        self.irq = int(tmp[5])
        self.softirq = int(tmp[6])
        self.load1 = int(tmp[0]) + int(tmp[2])
        self.load2 = int(tmp[0]) + int(tmp[2]) + int(tmp[3])
        return

    def toString(self) -> str:
        load: float = self.load1 * float(100) / self.load2
        return format(load, ".1f") + "%"


class cpu:
    name: str
    gloabal: float
    freq: list[subCpu]
    def __init__(self):
        self.freq = list[subCpu]()
        self.name = self.getName()
        first: list[subCpu] = self.getList()
        time.sleep(1)
        second: list[subCpu] = self.getList()

        self.gloabal = (second[0].load1 - first[0].load1) * float(100) / (second[0].load2 - first[0].load2)
        for i in range(1, len(first)):
            self.freq.append(
                subCpu(
                    second[i].user - first[i].user,
                    second[i].nice - first[i].nice,
                    second[i].system - first[i].system,
                    second[i].idle - first[i].idle,
                    second[i].iowait - first[i].iowait,
                    second[i].irq - first[i].irq,
                    second[i].softirq - first[i].softirq,
                    second[i].load1 - first[i].load1,
                    second[i].load2 - first[i].load2,
                )
            )
        return

    def getName(self):
        file = ""
        with open("/proc/cpuinfo") as f:
            for line in f:
                file += line
        for it in file.split("\n\n"):
            for line in it.split("\n"):
                try:
                    (key, val) = line.split("\t: ")
                    keyName = key.rstrip()
                    if (keyName == "model name"):
                        return val
                except (ValueError):
                    pass
        return ""

    def getList(self) -> list[subCpu]:
        file = []
        with open("/proc/stat") as f:
            for line in f:
                tmp = line.split(" ")
                if ("cpu" in tmp[0]):
                    file.append(line)
        listVal = []
        for it in file:
            builder: subCpu = subCpu(0, 0, 0, 0, 0, 0, 0, 0, 0)
            tmp = it.split(" ")
            try:
                tmp.remove("")
            except Exception:
                tmp = tmp
            tmp.remove(tmp[0])
            builder.initWith(tmp)
            listVal.append(builder)
        return listVal

    def toString(self) -> str:
        return "cpu: " + format(self.gloabal, ".1f") + "% - " + self.name

class user:
    name: str
    host: str
    def __init__(self):
        self.name = getpass.getuser()
        self.host = socket.gethostname()
    def toString(self) -> str:
        return self.name + " - " + self.host