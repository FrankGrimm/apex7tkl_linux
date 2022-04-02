from matplotlib import use
from hardware import cpu, memory, user


class cinematicTextDynamic:
    def __init__(self, text: str, max: int, c: int):
        self.txt = text
        self.offset = 0
        self.max = max
        self.char = chr(c)

    def isEnded(self) -> bool:
        return (self.max + len(self.txt)) == self.offset

    def restart(self):
        self.offset = 0

    def next(self):
        if (self.isEnded() == False):
            self.offset += 1

    def display(self) -> str:
        return (self.char * self.max + self.txt + self.char * self.max)[self.offset:self.offset + self.max]

class cinematicTextStatic:
    def __init__(self, text: str, step: int, max: int):
        self.txt = text
        self.offset = 0
        self.step = step
        self.max = max

    def isEnded(self) -> bool:
        return self.step == self.offset

    def restart(self):
        self.offset = 0

    def next(self):
        if (self.isEnded() == False):
            self.offset += 1

    def display(self) -> str:
        txt = ("." * self.max + self.txt + "." * self.max)
        pos = int(float(len(txt) / 2) - float(self.max / 2))
        return txt[pos:pos + self.max]

class cinematicText:
    def __init__(self, text: str, step: int):
        self.txt = text
        self.offset = 0
        self.step = step

    def isEnded(self) -> bool:
        return self.step == self.offset

    def restart(self):
        self.offset = 0

    def next(self):
        if (self.isEnded() == False):
            self.offset += 1

    def display(self) -> str:
        return self.txt

class cinematicBlink:
    def __init__(self, src, iteration: int, step: int, blinkStat: bool):
        self.src = src
        self.offset = 0
        self.step = step
        self.it = iteration
        self.blink = blinkStat

    def isEnded(self) -> bool:
        return self.step * self.it == self.offset

    def restart(self):
        self.offset = 0
        self.src.restart()

    def next(self):
        if (self.isEnded() == False):
            self.offset += 1
            self.src.next()

    def display(self) -> str:
        default = self.src.display()
        iter = (self.offset - (self.offset % self.it)) / self.it
        if iter % 2 == 1:
            if self.blink:
                return " " * len(default)
            else:
                return "#" * len(default)
        return default

class cinematicManager:
    def __init__(self):
        self.list = []

    def isEnded(self) -> bool:
        for it in self.list:
            if it.isEnded() == False:
                return False
        return True

    def restart(self):
        for it in self.list:
            it.restart()

    def next(self):
        for it in self.list:
            if (it.isEnded() == False):
                it.next()

    def display(self) -> str:
        data = []
        for it in self.list:
            data += [it.display()]
        return "\n".join(data).strip()

class cinematicScene:
    def __init__(self):
        self.list = []

    def isEnded(self) -> bool:
        for it in self.list:
            if it.isEnded() == False:
                return False
        return True

    def restart(self):
        for it in self.list:
            it.restart()

    def next(self):
        for it in self.list:
            if (it.isEnded() == False):
                it.next()
                return

    def display(self) -> str:
        for it in self.list:
            if (it.isEnded() == False):
                return it.display()
        return self.list[-1].display()

def DefaultHardwareCinematic(cpuInfo: cpu, usrInfo: user, memInfo: memory) -> cinematicScene:
    mng = cinematicScene()
    scnSrt = cinematicManager()
    scnUsr = cinematicManager()
    scnMem = cinematicManager()
    scnRam = cinematicManager()
    scnSwp = cinematicManager()
    scnCpu = cinematicManager()
    scnEnd = cinematicManager()

    scnSrt.list = [
        cinematicTextStatic("Powered", 21, 21),
        cinematicTextStatic("by", 21, 21),
        cinematicTextStatic("Sullmin && FrankGrimm", 21, 21),
        ]
    scnEnd.list = [
        cinematicBlink(cinematicTextStatic("", 21, 21), 2, 10, True),
        cinematicBlink(cinematicTextStatic("Restart Soon", 21, 21), 2, 10, True),
        cinematicBlink(cinematicTextStatic("", 21, 21), 2, 10, True),
        ]

    scnUsr.list = [
        cinematicTextStatic("Who", 21, 21),
        cinematicTextDynamic("User: " + usrInfo.name, 21, 46),
        cinematicTextDynamic("Host: " + usrInfo.host, 21, 46),
        ]
    scnMem.list = [
        cinematicTextStatic("Memory", 21, 21),
        cinematicTextStatic("Ram " + format((memInfo.ram.total - memInfo.ram.free) * 100 / memInfo.ram.total, ".1f") + "%", 20, 21),
        cinematicTextStatic("Swap " + format((memInfo.swap.total - memInfo.swap.free) * 100 / memInfo.swap.total, ".1f") + "%", 20, 21),
        ]
    scnRam.list = [
        cinematicTextStatic("Ram", 21, 21),
        cinematicTextStatic("Used: " + format(memInfo.ram.total - memInfo.ram.free, ".1f") + "G", 21, 21),
        cinematicTextStatic("Total: " + format(memInfo.ram.total, ".1f") + "G", 21, 21),
        ]
    scnSwp.list = [
        cinematicTextStatic("Swap", 21, 21),
        cinematicTextStatic("Used: " + format(memInfo.swap.total - memInfo.swap.free, ".1f") + "G", 21, 21),
        cinematicTextStatic("Total: " + format(memInfo.swap.total, ".1f") + "G", 21, 21),
        ]
    scnCpu.list = [
        cinematicTextStatic("Cpu", 21, 21),
        cinematicTextStatic("Core: " + str(len(cpuInfo.freq)), 21, 21),
        cinematicTextDynamic(cpuInfo.name, 21, 46)
        ]

    mng.list = [
        scnSrt,
        scnUsr,
        scnMem,
        scnRam,
        scnSwp,
        scnCpu,
    ]

    for idx, it in enumerate(cpuInfo.freq):
        new = cinematicManager()
        load = it.load1 * 100 / it.load2

        new.list = [
            cinematicTextStatic("Core N°" + str(idx), 5, 21),
            cinematicTextStatic(format(load, ".1f") + "%", 5, 21),
            cinematicTextStatic("", 5, 21),
        ]
        mng.list.append(new)

    mng.list.append(scnEnd)
    return mng