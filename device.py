import os
import sys
import traceback

os.environ['LIBUSB_DEBUG'] = 'debug'
import usb.core
from usb.core import USBError
import usb.util

import oled

DEFAULT_LEN = 642

TARGETS = {"apex7tkl": {"idVendor": 0x1038, "idProduct": 0x1618}}

def find_device(target_name="apex7tkl"):
    target = TARGETS[ target_name ]

    print("%s => idVendor %s idProduct %s" % (target_name, target['idVendor'], target['idProduct']))

    try:
        dev = usb.core.find(idVendor = target['idVendor'], idProduct = target['idProduct'])
    except USBError as e:
        print("usb::find failed", e)

    if dev is None:
        raise Exception("target device %s not found" % target_name)

    target['name'] = target_name
    return target, dev

def detach_kernel(dev):
    was_detached = set()
    for config in dev:
        for iface in range(config.bNumInterfaces):
            if dev.is_kernel_driver_active(iface) == True:
                was_detached.add(iface)
                print("dev::detach_kernel_driver(%s)" % iface)
                try:
                    dev.detach_kernel_driver(iface)
                except USBError as e:
                    print("dev::detach_kernel_driver(%s) failed" % iface, e)
    return was_detached

def reattach_kernel(dev, was_detached):
    print("dev::dispose_resources")
    usb.util.dispose_resources(dev)
    if len(was_detached) > 0:
        for iface in was_detached:
            print("dev::attach_kernel_driver(%s)" % iface)
            dev.attach_kernel_driver(iface)

def set_configuration(dev):
    try:
        print("dev::set_configuration")
        dev.set_configuration()
    except USBError as e:
        print(e)

class Device():

    def __init__ (self, target_name = "apex7tkl"):
        self.target_name = target_name
        self.target = None
        self.handle = None
        self._was_detached = None

    def __enter__ (self):
        self.target, self.handle = find_device(target_name = self.target_name)
        self._was_detached = detach_kernel(self.handle)
        set_configuration(self.handle)
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
        report = oled.OLED_PREAMBLE + imagedata
        self.send(0x300, 0x01, report)

    def oled_text(self, text):
        imagedata = oled.text_payload(text)
        report = oled.OLED_PREAMBLE + imagedata
        self.send(0x300, 0x01, report)

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

