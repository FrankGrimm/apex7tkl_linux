import os
import sys
from time import sleep
import traceback
from cinematic import cinematicBlink, cinematicManager, cinematicScene, cinematicText, cinematicTextStatic, cinematicTextDynamic

from hardware import cpu, memory, user

os.environ['LIBUSB_DEBUG'] = 'debug'
import usb.core
from usb.core import USBError
import usb.util

import oled

DEFAULT_LEN = 642

TARGETS = [
    { "name": "apex7", "idVendor": 0x1038, "idProduct": 0x1612 },
    { "name": "apex7tkl", "idVendor": 0x1038, "idProduct": 0x1618 },
    { "name": "apex5", "idVendor": 0x1038, "idProduct": 0x161c },
]

def find_device():
    """Find the first matching keyboard device in the TARGETS list"""

    for target in TARGETS:
        try:
            dev = usb.core.find(idVendor = target['idVendor'], idProduct = target['idProduct'])
            if dev is not None:
                return target, dev
        except USBError as e:
            print(f"usb::find({target['name']}) failed: {e}")

    raise Exception("Cannot find a matching device")

def detach_kernel(dev):
    if dev.is_kernel_driver_active(1) == True:
        try:
            print("dev::detach_kernel_driver - interface 1")
            dev.detach_kernel_driver(1)
            return True
        except USBError as e:
            print("dev::detach_kernel_driver failed" + str(e))
    return False

def reattach_kernel(dev, was_detached):
    print("dev::dispose_resources")
    usb.util.dispose_resources(dev)
    if was_detached:
        try:
            print("dev::artach_kernel_driver - interface 1")
            dev.attach_kernel_driver(1)
        except USBError as e:
            print("dev::attach_kernel_driver failed" + str(e))

class Device():
    def __init__ (self):
        self.target = None
        self.handle = None
        self._was_detached = None

    def __enter__ (self):
        self.target, self.handle = find_device()
        self._was_detached = detach_kernel(self.handle)
        return self

    def __exit__ (self, type, value, tb):
        reattach_kernel(self.handle, self._was_detached)


    def pad(self, payload, maxlen=642):
        if len(payload) < maxlen:
            payload += [0x00] * (maxlen - len(payload))
        return payload

    def send(self, wValue = 0x300, reqType = 0x01, payload=None):
        if payload is None:
            raise Exception("payload cannot be null")
        self.handle.ctrl_transfer(0x21,
                0x09,
                wValue,
                reqType,
                payload)

    def send_colors(self, color_payload):
        report = [0x3a, 0x69] + color_payload
        report = self.pad(report, DEFAULT_LEN)
        self.send(0x300, 0x01, report)

    def set_config(self, config_id):
        report = [0x89] + [config_id]
        report = self.pad(report, 20)
        self.send(0x200, 0x01, report)

    def oled_blank(self, filename="./images/blank.png"):
        self.oled_image(filename)

    def oled_image(self, filename):
        imagedata = oled.image_to_payload(filename)
        if imagedata is list[int]:
            report = oled.OLED_PREAMBLE + imagedata
            self.send(0x300, 0x01, report)
        else:
            while True:
                for it in imagedata:
                    report = oled.OLED_PREAMBLE + it
                    sleep(0.1)
                    self.send(0x300, 0x01, report)

    def oled_text(self, text):
        imagedata = oled.text_payload(text)
        report = oled.OLED_PREAMBLE + imagedata
        self.send(0x300, 0x01, report)

    def oled_monitor(self):
        cpuInfo = cpu()
        usrInfo = user()
        memInfo = memory()
        mng = cinematicScene()

        scn1 = cinematicManager()
        scn2 = cinematicManager()
        scn3 = cinematicManager()
        scn4 = cinematicManager()
        scn5 = cinematicManager()

        ## scn1.list = [cinematicBlink(cinematicText("scene1", 21, 42), 5, 4, True)]
        scn1.list = [
            cinematicTextStatic("Who", 21, 21),
            cinematicTextDynamic("Host: " + usrInfo.host, 21, 46),
            cinematicTextDynamic("User: " + usrInfo.name, 21, 46),
            ]
        scn2.list = [
            cinematicTextStatic("Memory", 21, 21),
            cinematicBlink(cinematicTextStatic("ram", 20, 21), 2, 10, False),
            cinematicBlink(cinematicTextStatic("swap", 20, 21), 2, 10, False),
            ]
        scn3.list = [
            cinematicTextStatic("Ram", 21, 21)
            ]
        scn4.list = [
            cinematicTextStatic("Swap", 21, 21)
            ]
        scn5.list = [
            cinematicTextStatic("Cpu", 21, 21),
            cinematicTextStatic("Core: " + str(len(cpuInfo.freq)), 21, 21),
            cinematicTextDynamic(cpuInfo.name, 21, 46)
            ]

        mng.list = [
            scn1,
            scn2,
            scn3,
            scn4,
            scn5,
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

        while True:
            print("RESTART")
            mng.restart()
            while mng.isEnded() == False:
                for _ in range(0, 3):
                    msg = mng.display()
                    print("MSG START")
                    print(msg)
                    print("MSG END")
                    imagedata = oled.text_payload(msg)
                    report = oled.OLED_PREAMBLE + imagedata
                    self.send(0x300, 0x01, report)
                    sleep(0.1)
                print("NEXT")
                mng.next()
            print("UPDATE")
            usrInfo.update()
            memInfo.update()
            cpuInfo.update()

#printimage(full)
#payload_to_image(full, "payload.png")
#loaded = image_to_payload("payload.png")
#printimage(loaded)
#
#printimage(text_payload("Hello World\nLine 2\nLine3"))
#printimage(text_payload("Hello World\nLine 2\nOverflow 12345678901234567890"))
#

#cfg = dev.get_active_configuration()
#print("config", cfg)
#intf = cfg[(0, 0)]
#
#ep = usb.util.find_descriptor(intf,
#        custom_match = \
#            lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)
#
#print("endpoint", ep)

