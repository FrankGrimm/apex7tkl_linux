KEYMAP = {}

KEYS_ALPHA = [kc + 0x04 for kc in range(25+1)] # A-Z in order
for idx, character in enumerate([chr(ord('A') + kc) for kc in range(25+1)]):
    KEYMAP[ character ] = KEYS_ALPHA[ idx ]
KEYS_NUMERIC = [kc + 0x1e for kc in range(10+1)] # 1,2,3,4,5,6,7,8,9,0 in order
for idx, character in enumerate([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]):
    KEYMAP[ str(character) ] = KEYS_NUMERIC[ idx ]

KEYS_FKEYS = []
for fkey, kc in [("F%s" % (i+1), 0x3A + i) for i in range(12)]:
    KEYMAP[ fkey ] = kc
    KEYS_FKEYS.append(kc)

KEYS_SPECIAL = {}

KEYS_SPECIAL[ "`" ] = 0x35
KEYS_SPECIAL[ "~" ] = 0x35
KEYS_SPECIAL[ "ESC" ] = 0x29
KEYS_SPECIAL[ "BACKSPACE" ] = 0x2A
KEYS_SPECIAL[ "TAB" ] = 0x2B
KEYS_SPECIAL[ "-" ] = 0x2D
KEYS_SPECIAL[ "_" ] = 0x2D
KEYS_SPECIAL[ "+" ] = 0x2E
KEYS_SPECIAL[ "=" ] = 0x2E
KEYS_SPECIAL[ "[" ] = 0x2F
KEYS_SPECIAL[ "{" ] = 0x2F
KEYS_SPECIAL[ "]" ] = 0x30
KEYS_SPECIAL[ "}" ] = 0x30
KEYS_SPECIAL[ ":" ] = 0x33
KEYS_SPECIAL[ ";" ] = 0x33
KEYS_SPECIAL[ "'" ] = 0x34
KEYS_SPECIAL[ "|" ] = 0x34
KEYS_SPECIAL[ "<" ] = 0x36
KEYS_SPECIAL[ "," ] = 0x36
KEYS_SPECIAL[ ">" ] = 0x37
KEYS_SPECIAL[ "." ] = 0x37
KEYS_SPECIAL[ "/" ] = 0x38
KEYS_SPECIAL[ "?" ] = 0x38
KEYS_SPECIAL[ "CAPSLOCK" ] = 0x39
KEYS_SPECIAL[ "M1" ] = 0x49
KEYS_SPECIAL[ "INS" ] = 0x49
KEYS_SPECIAL[ "M2" ] = 0x4A
KEYS_SPECIAL[ "HOME" ] = 0x4A
KEYS_SPECIAL[ "M3" ] = 0x4B
KEYS_SPECIAL[ "PG_UP" ] = 0x4B
KEYS_SPECIAL[ "M4" ] = 0x4C
KEYS_SPECIAL[ "DEL" ] = 0x4C
KEYS_SPECIAL[ "M5" ] = 0x4D
KEYS_SPECIAL[ "END" ] = 0x4D
KEYS_SPECIAL[ "M6" ] = 0x4E
KEYS_SPECIAL[ "PG_DN" ] = 0x4E
KEYS_SPECIAL[ "ARROW_RIGHT" ] = 0x4F
KEYS_SPECIAL[ "ARROW_LEFT" ] = 0x50
KEYS_SPECIAL[ "ARROW_DOWN" ] = 0x51
KEYS_SPECIAL[ "ARROW_UP" ] = 0x52
KEYS_SPECIAL[ "CTRL_LEFT" ] = 0xE0
KEYS_SPECIAL[ "SHIFT_LEFT" ] = 0xE1
KEYS_SPECIAL[ "ALT_LEFT" ] = 0xE2
KEYS_SPECIAL[ "WIN_LEFT" ] = 0xE3
KEYS_SPECIAL[ "CTRL_RIGHT" ] = 0xE4
KEYS_SPECIAL[ "SHIFT_RIGHT" ] = 0xE5
KEYS_SPECIAL[ "ALT_RIGHT" ] = 0xE6
KEYS_SPECIAL[ "WIN_RIGHT" ] = 0xE7
KEYS_SPECIAL[ "STEEL_META" ] = 0xF0
KEYS_SPECIAL[ " " ] = 0x2C
KEYS_SPECIAL[ "SPACE" ] = 0x2C
KEYS_SPECIAL[ "RETURN" ] = 0x28
KEYS_SPECIAL[ "\\" ] = 0x32
KEYS_SPECIAL[ "\"" ] = 0x32
KEYS_SPECIAL[ "<" ] = 0x64
KEYS_SPECIAL[ ">" ] = 0x64

for character, addr in KEYS_SPECIAL.items():
    KEYMAP[ character ] = addr

def get_key_codes(charmap):
    res = set()
    for char in charmap:
        if char in KEYS_SPECIAL:
            res.add(KEYS_SPECIAL[char])
    return res

KEY_REGIONS = {}
KEY_REGIONS['FKEYS'] = KEYS_FKEYS
KEY_REGIONS['ALPHA'] = KEYS_ALPHA + list(get_key_codes(["SPACE"]))
KEY_REGIONS['NUMERIC'] = KEYS_NUMERIC
KEY_REGIONS['SYMBOLS_LEFT'] = get_key_codes(["ESC", "`", "TAB", "CAPSLOCK", "SHIFT_LEFT", "CTRL_LEFT", "WIN_LEFT", "ALT_LEFT"])
KEY_REGIONS['SYMBOLS_RIGHT1'] = get_key_codes(["BACKSPACE", "RETURN", "-", "=", "[", "]", ";", "'", "\\", ",", ".", "/", "SHIFT_RIGHT", "CTRL_RIGHT", "WIN_RIGHT", "STEEL_META", "ALT_RIGHT"])
KEY_REGIONS['SYMBOLS_RIGHT2'] = get_key_codes(["M1", "M2", "M3", "M4", "M5", "M6", "ARROW_UP", "ARROW_DOWN", "ARROW_LEFT", "ARROW_RIGHT"])
KEY_REGIONS["ALL"] = set(KEYMAP.values())

def others(used_keycodes):
    return set(KEYMAP.values()) - set(used_keycodes)

def get(key):
    res = []
    if not key or key == '':
        return res

    if key.upper() in KEY_REGIONS.keys():
        res = list(KEY_REGIONS[key.upper()])
        return res

    if key in KEYMAP.keys():
        res.append(KEYMAP[key])

    return list(set(res))
