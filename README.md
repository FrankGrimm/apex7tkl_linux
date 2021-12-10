# Steelseries Apex 7 on Linux

This is raw and unpolished code. Use it at your own risk.

`ssere.py` contains examples on how to:
- Set key colors (individual or by region)
- Activate or switch a configuration
- Update the OLED image or write text to the display

## Installation

```pip install -r requirements.txt```

## Usage as non-root

This requires a `udev` ruleset.

```sudo cp 51-apex.rules /etc/udev/rules.d/51-apex.rules && sudo udevadm control --reload && sudo udevadm trigger```

## CLI usage

### Load profile

Takes in the the profile number.

- `./cli.py config 1`

### Oled screen control

- `./cli.py oledblank`
- `./cli.py oled ./images/grimm.png`
- `./cli.py oledtext "Hello" "from the other side"`

### Color

Takes in pairs of (keycode(s) or region(s), color). You can define multiple keycodes or regions in a given pair by using a comma separator.

Examples:

- `./cli.py color ALL orange`
- `./cli.py color ALPHA c26838`
- `./cli.py color F9,F10,F11,F12 red`
- `./cli.py color SYMBOLS_LEFT green F1,F2,F3,F4 red -- black`

Available regions:

- `FKEYS`: Function keys
- `ALPHA`: Letters and space bar
- `NUMERIC`: Number row
- `SYMBOLS_LEFT`: Symbols left of alpha keys
- `SYMBOLS_RIGHT1`: Symbols right of alpha keys
- `SYMBOLS_RIGHT2` M1 to M6 and arrow keys
- `KEYPAD`: Numeric key pad (not available for Apex7 TKL)
- `ALL`: All keys
- `--`: Special region that sets the following color on all keys that have not been used so far.

See `keys.py` for list key codes
