# Steelseries Apex 7 TKL on Linux

This is raw and unpolished code. Use it at your own risk.

`ssere.py` contains examples on how to:
- Set key colors (individual or by region)
- Activate or switch a configuration
- Update the OLED image or write text to the display

## installation

```pip install -r requirements.txt```

## Usage as non-root

This requires a `udev` ruleset.

```sudo cp 51-apex.rules /etc/udev/rules.d/51-apex.rules && sudo udevadm control --reload && sudo udevadm trigger```

## CLI usage

- `./cli.py config 1`
- `./cli.py oledblank`
- `./cli.py oled ./images/grimm.png`
- `./cli.py oledtext "Hello" "from the other side"`
- ` ./cli.py color SYMBOLS_LEFT green F1,F2,F3,F4 red -- black` set colors, takes in pairs of (keycode or region, color). The special region "--" sets the following color on all keys that have not been used so far. Definitions in `keys.py`.
- `./cli.py color ALL orange`
- `./cli.py color ALPHA c26838`
- `./cli.py color F9,F10,F11,F12 red`


## Other devices

Unclear, presumably the regular Apex 7 would also work (would need adjustment of the product ID and key map in `keys.py`).
