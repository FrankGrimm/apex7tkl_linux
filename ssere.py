import os
import sys
import traceback

import keys
import colors
import device

from time import sleep

from usb.core import USBError

with device.Device() as device:
    for idx in range(5):
        device.oled_text("GRIMM---\n   %s   \n#######" % idx)
        sleep(1.0)
    device.oled_blank()
    sleep(2)
    device.oled_image("./images/grimm.png")

def switch_configs(device):
    print("set_config(2)")
    device.set_config(2)
    sleep(5)
    print("set_config(1)")
    device.set_config(1)

def cycle_regions(device):
    for region, region_keys in keys.KEY_REGIONS.items():
        for color in [colors.COLOR_RED, colors.COLOR_GREEN, colors.COLOR_BLUE]:
            print("illuminating region", region, "color", color)
            COLOR_PAYLOAD = []
            for addr in region_keys:
                COLOR_PAYLOAD += [addr]
                COLOR_PAYLOAD += color
            for addr in keys.others(region_keys):
                COLOR_PAYLOAD += [addr]
                COLOR_PAYLOAD += colors.COLOR_BLACK

            device.send_colors(COLOR_PAYLOAD)
            sleep(0.8)

def cycle_allkeys(device):
    seen = set()
    for cur in set(keys.KEYMAP.values()):
        continue
        sleep(0.1)
        print("cur", hex(cur))
    for idx in range(5):
        device.oled
        sleep(1.0)
        seen.add(cur)

        try:
            COLOR_PAYLOAD = []

    #        COLOR_PAYLOAD = [KEY_ADDR[tgt_idx]] + colors.COLOR_ORANGE
            for addr in set(keys.KEYMAP.values()):
                COLOR_PAYLOAD.append(addr)

                if addr in seen:
                    COLOR_PAYLOAD += colors.COLOR_ORANGE
                else:
                    COLOR_PAYLOAD += colors.COLOR_BLACK

            device.send_colors(COLOR_PAYLOAD)
            print("sending report done")
        except USBError as e:
            print("failed to send report", e)
            traceback.print_exc()
        except Exception as e1:
            print("generic error", e1)

