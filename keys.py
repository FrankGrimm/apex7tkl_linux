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

KEYS_KEYPAD = {
    "NUMLOCK": 0x53,     # Num Lock/Clear
    "KP_SLASH": 0x54,    # /
    "KP_ASTERISK": 0x55, # *
    "KP_MINUS": 0x56,    # -
    "KP_PLUS": 0x57,     # +
    "KP_ENTER": 0x58,    # Enter
    "KP_1": 0x59,        # 1, End
    "KP_2": 0x5a,        # 2, Down Arrow
    "KP_3": 0x5b,        # 3, PageDn
    "KP_4": 0x5c,        # 4, Left Arrow
    "KP_5": 0x5d,        # 5
    "KP_6": 0x5e,        # 6, Right Arrow
    "KP_7": 0x5f,        # 7, Home
    "KP_8": 0x60,        # 8, Up Arrow
    "KP_9": 0x61,        # 9, Page Up
    "KP_0": 0x62,        # 0, Insert
    "KP_DOT": 0x63,      # ., Delete
}
KEYMAP.update(KEYS_KEYPAD)

KEYS_SPECIAL = {
    "`": 0x35,
    "~": 0x35,
    "ESC": 0x29,
    "BACKSPACE": 0x2A,
    "TAB": 0x2B,
    "-": 0x2D,
    "_": 0x2D,
    "+": 0x2E,
    "=": 0x2E,
    "[": 0x2F,
    "{": 0x2F,
    "]": 0x30,
    "}": 0x30,
    ":": 0x33,
    ";": 0x33,
    "'": 0x34,
    "\"": 0x34,
    "<": 0x36,
    ",": 0x36,
    ">": 0x37,
    ".": 0x37,
    "/": 0x38,
    "?": 0x38,
    "CAPSLOCK": 0x39,
    "M1": 0x49,
    "INS": 0x49,
    "M2": 0x4A,
    "HOME": 0x4A,
    "M3": 0x4B,
    "PG_UP": 0x4B,
    "M4": 0x4C,
    "DEL": 0x4C,
    "M5": 0x4D,
    "END": 0x4D,
    "M6": 0x4E,
    "PG_DN": 0x4E,
    "ARROW_RIGHT": 0x4F,
    "ARROW_LEFT": 0x50,
    "ARROW_DOWN": 0x51,
    "ARROW_UP": 0x52,
    "CTRL_LEFT": 0xE0,
    "SHIFT_LEFT": 0xE1,
    "ALT_LEFT": 0xE2,
    "WIN_LEFT": 0xE3,
    "CTRL_RIGHT": 0xE4,
    "SHIFT_RIGHT": 0xE5,
    "ALT_RIGHT": 0xE6,
    "WIN_RIGHT": 0xE7,
    "STEEL_META": 0xF0,
    " ": 0x2C,
    "SPACE": 0x2C,
    "RETURN": 0x28,
    "\\": 0x31,
    "|": 0x31,
    "<": 0x64,
    ">": 0x64,
}

for character, addr in KEYS_SPECIAL.items():
    KEYMAP[ character ] = addr

def get_key_codes(charmap):
    res = set()
    for char in charmap:
        if char in KEYS_SPECIAL:
            res.add(KEYS_SPECIAL[char])
    return res

KEY_REGIONS = {
    "FKEYS": KEYS_FKEYS,
    "ALPHA": KEYS_ALPHA + list(get_key_codes(["SPACE"])),
    "NUMERIC": KEYS_NUMERIC,
    "SYMBOLS_LEFT": get_key_codes(["ESC", "`", "TAB", "CAPSLOCK", "SHIFT_LEFT", "CTRL_LEFT", "WIN_LEFT", "ALT_LEFT"]),
    "SYMBOLS_RIGHT1": get_key_codes(["BACKSPACE", "RETURN", "-", "=", "[", "]", ";", "'", "\\", ",", ".", "/", "SHIFT_RIGHT", "CTRL_RIGHT", "WIN_RIGHT", "STEEL_META", "ALT_RIGHT"]),
    "SYMBOLS_RIGHT2": get_key_codes(["M1", "M2", "M3", "M4", "M5", "M6", "ARROW_UP", "ARROW_DOWN", "ARROW_LEFT", "ARROW_RIGHT"]),
    "KEYPAD": KEYS_KEYPAD.values(),
    "ALL": set(KEYMAP.values()),
}

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
