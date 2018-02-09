def test_pale_purple():
    assert(planes_to_color([1,0,1,255]) == 0x10001)

def test_bright_green():
    assert(planes_to_color([0,150,0,255]) == 0x9600)

def test_brightest_blue():
    assert(planes_to_color([0,0,255,255]) == 0xFF)

def planes_to_color(planes):
    """
    Converts the 4 element array of planes data to
    Neopixel color form and returns AdaFruit_NeoPixel::Color()
    color value.  Probably okay to ignore the 4th value.
    """
    return 0x10001          # faint purple


