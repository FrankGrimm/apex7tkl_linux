
COLOR_BLACK = [0x00, 0x00, 0x00]
COLOR_RED = [0xff, 0x00, 0x00]
COLOR_GREEN = [0x00, 0xff, 0x00]
COLOR_BLUE = [0x00, 0x00, 0xff]
COLOR_ORANGE = [0xff, 0x52, 0x00]

_KNOWN = {"red": "ff0000", "green": "00ff00", "blue": "0000ff", "black": "000000", "white": "ffffff", "orange": "ff5200"}

def get(t):
    t = t.lower()
    if t in _KNOWN:
        t = _KNOWN[t]

    if len(t) != 6:
        raise Exception("only RRGGBB format is currently supported")

    r,g,b = t[0:2], t[2:4], t[4:6]
    col = [ int(r, 16), int(g, 16), int(b, 16) ]
    return col

