import os
import sys

import usb.core
from usb.core import USBError
import usb.util

os.environ['LIBUSB_DEBUG'] = 'debug'


TARGETS = {"apex7tkl": {"idVendor": 0x1038, "idProduct": 0x1618}}

target_device = None
for target_name, target in TARGETS.items():
    print("idVendor %s idProduct %s" % (target['idVendor'], target['idProduct']))
    dev = usb.core.find(idVendor = target['idVendor'], idProduct = target['idProduct'])
    if dev is None:
        continue
    target['name'] = target_name
    target_device = target
    target_device['handle'] = dev
    break

if target_device is None:
    print("device not found")
    sys.exit(1)

print("found target device %s" % ( target_device['name'] ))
dev = target_device['handle']

was_detached = False
if dev.is_kernel_driver_active(0) == True:
    was_detached = True
    print("dev::detach_kernel_driver")
    try:
        dev.detach_kernel_driver(0)
    except USBError as e:
        print("dev::detach_kernel_driver failed", e)

print("dev::dispose_resources")
usb.util.dispose_resources(dev)
